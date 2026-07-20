from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from django.contrib.messages import get_messages
from statuses.models import Status
from labels.models import Label
from .models import Task


class TaskCRUDTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.author = User.objects.create_user(username='author', password='pass123')
        self.other_user = User.objects.create_user(username='other', password='pass123')
        self.status = Status.objects.create(name='New')
        self.task = Task.objects.create(
            name='Test Task',
            description='Desc',
            status=self.status,
            author=self.author
        )
        self.create_url = reverse('tasks_create')
        self.update_url = reverse('tasks_update', kwargs={'pk': self.task.pk})
        self.delete_url = reverse('tasks_delete', kwargs={'pk': self.task.pk})
        self.detail_url = reverse('tasks_detail', kwargs={'pk': self.task.pk})
        self.list_url = reverse('tasks_list')

    def test_list_requires_login(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, 302)
        self.assertIn('/login/', response.url)

    def test_create_task_success(self):
        self.client.login(username='author', password='pass123')
        response = self.client.post(self.create_url, {
            'name': 'New Task',
            'description': 'Desc',
            'status': self.status.pk,
        })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.list_url)
        self.assertTrue(Task.objects.filter(name='New Task', author=self.author).exists())

    def test_update_task_success(self):
        self.client.login(username='author', password='pass123')
        response = self.client.post(self.update_url, {
            'name': 'Updated Task',
            'description': 'New Desc',
            'status': self.status.pk,
        })
        self.assertEqual(response.status_code, 302)
        self.task.refresh_from_db()
        self.assertEqual(self.task.name, 'Updated Task')

    def test_delete_task_by_author_success(self):
        self.client.login(username='author', password='pass123')
        response = self.client.post(self.delete_url)
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Task.objects.filter(name='Test Task').exists())

    def test_delete_task_by_non_author_fails(self):
        self.client.login(username='other', password='pass123')
        response = self.client.post(self.delete_url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.list_url)
        self.assertTrue(Task.objects.filter(name='Test Task').exists())
        
        messages = list(get_messages(response.wsgi_request))
        self.assertIn('Only the author can delete the task', str(messages[0]))

    def test_detail_requires_login(self):
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, 302)
        self.assertIn('/login/', response.url)

    def test_filter_by_status(self):
        self.client.login(username='author', password='pass123')
        status2 = Status.objects.create(name='In Progress')
        task2 = Task.objects.create(name='Task 2', status=status2, author=self.author)
        
        # Фильтруем по первому статусу
        response = self.client.get(self.list_url + f'?status={self.status.pk}')
        self.assertContains(response, 'Test Task')
        self.assertNotContains(response, 'Task 2')

    def test_filter_by_assignee(self):
        self.client.login(username='author', password='pass123')
        task2 = Task.objects.create(name='Task 2', status=self.status, author=self.author, assignee=self.other_user)
        
        response = self.client.get(self.list_url + f'?assignee={self.other_user.pk}')
        self.assertContains(response, 'Task 2')
        self.assertNotContains(response, 'Test Task')

    def test_filter_by_label(self):
        self.client.login(username='author', password='pass123')
        label1 = Label.objects.create(name='bug')
        label2 = Label.objects.create(name='feature')
        
        task1 = Task.objects.create(name='Task 1', status=self.status, author=self.author)
        task1.labels.add(label1)
        
        task2 = Task.objects.create(name='Task 2', status=self.status, author=self.author)
        task2.labels.add(label2)
        
        response = self.client.get(self.list_url + f'?labels={label1.pk}')
        self.assertContains(response, 'Task 1')
        self.assertNotContains(response, 'Task 2')

    def test_filter_only_my_tasks(self):
        self.client.login(username='author', password='pass123')
        # Задача другого пользователя
        Task.objects.create(name='Other Task', status=self.status, author=self.other_user)
        
        # ИСПРАВЛЕНО: используем True вместо 'on' для надежной работы BooleanFilter
        response = self.client.get(self.list_url + '?only_my_tasks=True')
        self.assertContains(response, 'Test Task')
        self.assertNotContains(response, 'Other Task')