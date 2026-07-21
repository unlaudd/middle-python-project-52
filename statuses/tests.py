"""
Tests for status CRUD operations.

This module contains comprehensive test cases for verifying the complete
CRUD (Create, Read, Update, Delete) functionality of task statuses,
including authentication requirements, successful operations, and
proper flash message handling.
"""
from django.contrib.auth.models import User
from django.contrib.messages import get_messages
from django.test import Client, TestCase
from django.urls import reverse

from .models import Status


class StatusListViewTest(TestCase):
    """
    Test suite for status list view functionality.

    Verifies that the status list view properly handles authentication
    requirements and displays all existing statuses to authenticated users.

    Test Cases:
        - Unauthenticated users are redirected to login page
        - Authenticated users can view the status list with all statuses
    """

    def setUp(self):
        """
        Set up test fixtures for status list view tests.

        Creates:
            - Test client for making HTTP requests
            - Test user for authentication
            - Test status ('New') for list verification
            - URL reference for the statuses list endpoint
        """
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpassword123')
        self.status = Status.objects.create(name='New')
        self.url = reverse('statuses_list')

    def test_requires_login(self):
        """
        Verify that unauthenticated users are redirected to login.

        Expected Behavior:
            - GET request to statuses_list without authentication returns 302
            - Redirect URL contains '/login/' path

        This ensures that the status list view is protected and requires
        user authentication before displaying any data.
        """
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)
        self.assertIn('/login/', response.url)

    def test_list_accessible_for_authenticated(self):
        """
        Verify that authenticated users can view the status list.

        Expected Behavior:
            - GET request to statuses_list with authentication returns 200
            - Response contains the status name 'New'

        This ensures that authenticated users have proper access to view
        all available task statuses in the system.
        """
        self.client.login(username='testuser', password='testpassword123')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'New')


class StatusCreateViewTest(TestCase):
    """
    Test suite for status creation functionality.

    Verifies that the status creation view properly handles authentication
    requirements and allows authenticated users to create new statuses
    with appropriate success messaging.

    Test Cases:
        - Unauthenticated users are redirected to login page
        - Authenticated users can create new statuses successfully
        - Success flash message is displayed after creation
    """

    def setUp(self):
        """
        Set up test fixtures for status creation tests.

        Creates:
            - Test client for making HTTP requests
            - Test user for authentication
            - URL reference for the status creation endpoint
        """
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpassword123')
        self.url = reverse('statuses_create')

    def test_requires_login(self):
        """
        Verify that unauthenticated users are redirected to login.

        Expected Behavior:
            - GET request to statuses_create without authentication returns 302

        This ensures that the status creation view is protected and requires
        user authentication before allowing any creation operations.
        """
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)

    def test_create_status_success(self):
        """
        Verify that authenticated users can create new statuses successfully.

        Expected Behavior:
            - POST request with valid status data returns 302 redirect
            - Redirect target is the statuses list page
            - New status 'In Progress' is created in the database
            - Success flash message 'successfully created' is displayed

        This ensures that the status creation workflow functions correctly
        and provides appropriate user feedback.
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
    Test suite for status update functionality.

    Verifies that authenticated users can successfully update existing
    statuses with appropriate success messaging.

    Test Cases:
        - Authenticated users can update status names successfully
        - Success flash message is displayed after update
    """

    def setUp(self):
        """
        Set up test fixtures for status update tests.

        Creates:
            - Test client for making HTTP requests
            - Test user for authentication
            - Test status ('New') for update verification
            - URL reference for the status update endpoint
        """
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpassword123')
        self.status = Status.objects.create(name='New')
        self.url = reverse('statuses_update', kwargs={'pk': self.status.pk})

    def test_update_status_success(self):
        """
        Verify that authenticated users can update status names successfully.

        Expected Behavior:
            - POST request with updated status data returns 302 redirect
            - Status name in database is updated to 'Updated'
            - Success flash message 'successfully updated' is displayed

        This ensures that the status update workflow functions correctly
        and provides appropriate user feedback.
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
    Test suite for status deletion functionality.

    Verifies that authenticated users can successfully delete existing
    statuses with proper database cleanup.

    Test Cases:
        - Authenticated users can delete statuses successfully
        - Status is removed from database after deletion
    """

    def setUp(self):
        """
        Set up test fixtures for status deletion tests.

        Creates:
            - Test client for making HTTP requests
            - Test user for authentication
            - Test status ('New') for deletion verification
            - URL reference for the status deletion endpoint
        """
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpassword123')
        self.status = Status.objects.create(name='New')
        self.url = reverse('statuses_delete', kwargs={'pk': self.status.pk})

    def test_delete_status_success(self):
        """
        Verify that authenticated users can delete statuses successfully.

        Expected Behavior:
            - POST request to delete endpoint returns 302 redirect
            - Redirect target is the statuses list page
            - Status 'New' is removed from the database

        This ensures that the status deletion workflow functions correctly
        and properly cleans up database records.
        """
        self.client.login(username='testuser', password='testpassword123')
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('statuses_list'))
        self.assertFalse(Status.objects.filter(name='New').exists())
