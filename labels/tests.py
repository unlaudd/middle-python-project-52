from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from django.contrib.messages import get_messages
from statuses.models import Status
from tasks.models import Task
from .models import Label


class LabelCRUDTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='pass123')
        self.label = Label.objects.create(name='bug')
        self.create_url = reverse('labels_create')
        self.update_url = reverse('labels_update', kwargs={'pk': self.label.pk})
        self.delete_url = reverse('labels_delete', kwargs={'pk': self.label.pk})
        self.list_url = reverse('labels_list')

    def test_list_requires_login(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, 302)
        self.assertIn('/login/', response.url)

    def test_create_label_success(self):
        self.client.login(username='testuser', password='pass123')
        response = self.client.post(self.create_url, {'name': 'feature'})
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.list_url)
        self.assertTrue(Label.objects.filter(name='feature').exists())

    def test_update_label_success(self):
        self.client.login(username='testuser', password='pass123')
        response = self.client.post(self.update_url, {'name': 'updated_bug'})
        self.assertEqual(response.status_code, 302)
        self.label.refresh_from_db()
        self.assertEqual(self.label.name, 'updated_bug')

    def test_delete_label_success(self):
        self.client.login(username='testuser', password='pass123')
        response = self.client.post(self.delete_url)
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Label.objects.filter(name='bug').exists())

    def test_delete_label_linked_to_task_fails(self):
        self.client.login(username='testuser', password='pass123')
        status = Status.objects.create(name='New')
        task = Task.objects.create(
            name='Test Task',
            status=status,
            author=self.user
        )
        task.labels.add(self.label)
    
        # Проверка, что связь создана
        self.assertTrue(Task.objects.filter(labels=self.label).exists())
    
        response = self.client.post(self.delete_url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.list_url)
        self.assertTrue(Label.objects.filter(name='bug').exists())
    
        messages = list(get_messages(response.wsgi_request))
        self.assertIn('Unable to delete label', str(messages[0]))
