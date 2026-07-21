"""
Tests for label CRUD operations.

This module contains test cases for verifying the complete CRUD functionality
of the Label model, including creation, reading, updating, and deletion,
as well as protection against deleting labels that are linked to tasks.
"""
from django.contrib.auth.models import User
from django.contrib.messages import get_messages
from django.test import Client, TestCase
from django.urls import reverse

from statuses.models import Status
from tasks.models import Task

from .models import Label


class LabelCRUDTest(TestCase):
    """
    Test suite for label CRUD operations.

    This test class verifies that labels can be created, read, updated,
    and deleted correctly, and that labels linked to tasks cannot be deleted
    to maintain data integrity.

    Attributes:
        client (Client): Django test client for making HTTP requests.
        user (User): Test user for authenticated operations.
        label (Label): Test label instance.
        create_url (str): URL for label creation.
        update_url (str): URL for label update.
        delete_url (str): URL for label deletion.
        list_url (str): URL for label list.
    """

    def setUp(self):
        """
        Set up test fixtures.

        Creates a test client, authenticated user, test label, and
        initializes URL variables for CRUD operations.
        """
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='pass123')
        self.label = Label.objects.create(name='bug')
        self.create_url = reverse('labels_create')
        self.update_url = reverse('labels_update', kwargs={'pk': self.label.pk})
        self.delete_url = reverse('labels_delete', kwargs={'pk': self.label.pk})
        self.list_url = reverse('labels_list')

    def test_list_requires_login(self):
        """
        Test that label list view requires authentication.

        Verifies that unauthenticated users are redirected to the login page
        when attempting to access the label list.

        Expected:
            - Response status code: 302 (redirect)
            - Redirect URL contains '/login/'
        """
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, 302)
        self.assertIn('/login/', response.url)

    def test_create_label_success(self):
        """
        Test successful label creation by authenticated user.

        Verifies that an authenticated user can create a new label
        and is redirected to the label list after successful creation.

        Expected:
            - Response status code: 302 (redirect)
            - Redirect to label list URL
            - New label exists in database with name 'feature'
        """
        self.client.login(username='testuser', password='pass123')
        response = self.client.post(self.create_url, {'name': 'feature'})
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.list_url)
        self.assertTrue(Label.objects.filter(name='feature').exists())

    def test_update_label_success(self):
        """
        Test successful label update by authenticated user.

        Verifies that an authenticated user can update an existing label's name
        and is redirected to the label list after successful update.

        Expected:
            - Response status code: 302 (redirect)
            - Label name in database updated to 'updated_bug'
        """
        self.client.login(username='testuser', password='pass123')
        response = self.client.post(self.update_url, {'name': 'updated_bug'})
        self.assertEqual(response.status_code, 302)
        self.label.refresh_from_db()
        self.assertEqual(self.label.name, 'updated_bug')

    def test_delete_label_success(self):
        """
        Test successful label deletion by authenticated user.

        Verifies that an authenticated user can delete a label
        and is redirected to the label list after successful deletion.
        
        Expected:
            - Response status code: 302 (redirect)
            - Label with name 'bug' no longer exists in database
        """
        self.client.login(username='testuser', password='pass123')
        response = self.client.post(self.delete_url)
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Label.objects.filter(name='bug').exists())

    def test_delete_label_linked_to_task_fails(self):
        """
        Test that labels linked to tasks cannot be deleted.

        Verifies that attempting to delete a label that is associated with
        one or more tasks fails gracefully, displays an error message,
        and preserves both the label and the task-task relationship.

        Setup:
            - Creates a status, task, and associates the test label with the task.

        Expected:
            - Response status code: 302 (redirect)
            - Redirect to label list URL
            - Label with name 'bug' still exists in database
            - Error message 'Невозможно удалить метку' is displayed
        """
        self.client.login(username='testuser', password='pass123')
        status = Status.objects.create(name='New')
        task = Task.objects.create(
            name='Test Task',
            status=status,
            author=self.user
        )
        task.labels.add(self.label)

        self.assertTrue(Task.objects.filter(labels=self.label).exists())

        response = self.client.post(self.delete_url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.list_url)
        self.assertTrue(Label.objects.filter(name='bug').exists())

        messages = list(get_messages(response.wsgi_request))
        self.assertIn('Невозможно удалить метку', str(messages[0]))
