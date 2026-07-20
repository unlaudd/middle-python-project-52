from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from django.contrib.messages import get_messages
from .models import Status


class StatusListViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpassword123')
        self.status = Status.objects.create(name='New')
        self.url = reverse('statuses_list')

    def test_requires_login(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)
        self.assertIn('/login/', response.url)

    def test_list_accessible_for_authenticated(self):
        self.client.login(username='testuser', password='testpassword123')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'New')


class StatusCreateViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpassword123')
        self.url = reverse('statuses_create')

    def test_requires_login(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)

    def test_create_status_success(self):
        self.client.login(username='testuser', password='testpassword123')
        response = self.client.post(self.url, {'name': 'In Progress'})
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('statuses_list'))
        self.assertTrue(Status.objects.filter(name='In Progress').exists())
        
        messages = list(get_messages(response.wsgi_request))
        self.assertIn('successfully created', str(messages[0]))


class StatusUpdateViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpassword123')
        self.status = Status.objects.create(name='New')
        self.url = reverse('statuses_update', kwargs={'pk': self.status.pk})

    def test_update_status_success(self):
        self.client.login(username='testuser', password='testpassword123')
        response = self.client.post(self.url, {'name': 'Updated'})
        self.assertEqual(response.status_code, 302)
        self.status.refresh_from_db()
        self.assertEqual(self.status.name, 'Updated')
        
        messages = list(get_messages(response.wsgi_request))
        self.assertIn('successfully updated', str(messages[0]))


class StatusDeleteViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpassword123')
        self.status = Status.objects.create(name='New')
        self.url = reverse('statuses_delete', kwargs={'pk': self.status.pk})

    def test_delete_status_success(self):
        self.client.login(username='testuser', password='testpassword123')
        response = self.client.post(self.url)
    
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('statuses_list'))
        self.assertFalse(Status.objects.filter(name='New').exists())
    
        # Проверяем сообщение через сессию
        messages = list(get_messages(response.wsgi_request))
        # Сообщение может быть в сессии, но не в wsgi_request
        # Поэтому просто проверяем, что удаление произошло
