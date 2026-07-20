"""
Tests for status CRUD operations.
"""
from django.contrib.auth.models import User
from django.contrib.messages import get_messages
from django.test import Client, TestCase
from django.urls import reverse

from .models import Status


class StatusListViewTest(TestCase):
    """
    Test suite for status list view.
    """

    def setUp(self):
        """
        Set up test client, user, and status.
        """
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpassword123')
        self.status = Status.objects.create(name='New')
        self.url = reverse('statuses_list')

    def test_requires_login(self):
        """
        Unauthenticated users should be redirected to login.
        """
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)
        self.assertIn('/login/', response.url)

    def test_list_accessible_for_authenticated(self):
        """
        Authenticated users should be able to view the status list.
        """
        self.client.login(username='testuser', password='testpassword123')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'New')


class StatusCreateViewTest(TestCase):
    """
    Test suite for status creation.
    """

    def setUp(self):
        """
        Set up test client and user.
        """
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpassword123')
        self.url = reverse('statuses_create')

    def test_requires_login(self):
        """
        Unauthenticated users should be redirected to login.
        """
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)

    def test_create_status_success(self):
        """
        Authenticated users should be able to create a new status.
        """
        self.client.login(username='testuser', password='testpassword123')
        response = self.client.post(self.url, {'name': 'In Progress'})
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('statuses_list'))
        self.assertTrue(Status.objects.filter(name='In Progress').exists())

        messages = list(get_messages(response.wsgi_request))
        self.assertIn('successfully created', str(messages[0]))


class StatusUpdateViewTest(TestCase):
    """
    Test suite for status updates.
    """

    def setUp(self):
        """
        Set up test client, user, and status.
        """
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpassword123')
        self.status = Status.objects.create(name='New')
        self.url = reverse('statuses_update', kwargs={'pk': self.status.pk})

    def test_update_status_success(self):
        """
        Authenticated users should be able to update a status.
        """
        self.client.login(username='testuser', password='testpassword123')
        response = self.client.post(self.url, {'name': 'Updated'})
        self.assertEqual(response.status_code, 302)
        self.status.refresh_from_db()
        self.assertEqual(self.status.name, 'Updated')

        messages = list(get_messages(response.wsgi_request))
        self.assertIn('successfully updated', str(messages[0]))


class StatusDeleteViewTest(TestCase):
    """
    Test suite for status deletion.
    """

    def setUp(self):
        """
        Set up test client, user, and status.
        """
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpassword123')
        self.status = Status.objects.create(name='New')
        self.url = reverse('statuses_delete', kwargs={'pk': self.status.pk})

    def test_delete_status_success(self):
        """
        Authenticated users should be able to delete a status.
        """
        self.client.login(username='testuser', password='testpassword123')
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('statuses_list'))
        self.assertFalse(Status.objects.filter(name='New').exists())
