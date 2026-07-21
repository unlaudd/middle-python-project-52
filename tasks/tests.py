"""
Tests for the tasks application.

This module contains comprehensive test cases for verifying the complete
CRUD (Create, Read, Update, Delete) functionality of tasks, as well as
the task filtering capabilities (by status, assignee, label, and author).
"""
from django.contrib.auth.models import User
from django.contrib.messages import get_messages
from django.test import Client, TestCase
from django.urls import reverse

from labels.models import Label
from statuses.models import Status

from .models import Task


class TaskCRUDTest(TestCase):
    """
    Test suite for task CRUD operations and filtering.

    This test class verifies that tasks can be created, read, updated,
    and deleted correctly, with appropriate access controls (e.g., only
    the author can delete a task). It also verifies that the task list
    can be filtered by various criteria.

    Attributes:
        client (Client): Django test client for making HTTP requests.
        author (User): The user who authors the test tasks.
        other_user (User): A different user to test authorization boundaries.
        status (Status): A test status for the tasks.
        task (Task): A test task instance authored by the 'author' user.
        create_url (str): URL for task creation.
        update_url (str): URL for task update.
        delete_url (str): URL for task deletion.
        detail_url (str): URL for task detail view.
        list_url (str): URL for task list view.
    """

    def setUp(self):
        """
        Set up test data and URLs.

        Creates test users, a status, and a base task. Initializes
        URL references for all task-related CRUD endpoints.
        """
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
        """
        Test that unauthenticated users are redirected to the login page.

        Expected Behavior:
            - GET request to task list without authentication returns 302.
            - Redirect URL contains '/login/'.
        """
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, 302)
        self.assertIn('/login/', response.url)

    def test_create_task_success(self):
        """
        Test that authenticated users can successfully create a new task.

        Expected Behavior:
            - POST request with valid task data returns 302 redirect.
            - Redirect target is the task list page.
            - New task is created in the database with the correct author.
        """
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
        """
        Test that authenticated users can successfully update an existing task.

        Expected Behavior:
            - POST request with updated task data returns 302 redirect.
            - Task name and description in the database are updated.
        """
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
        """
        Test that the task author can successfully delete their own task.

        Expected Behavior:
            - POST request to delete endpoint by the author returns 302.
            - Task is removed from the database.
        """
        self.client.login(username='author', password='pass123')
        response = self.client.post(self.delete_url)
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Task.objects.filter(name='Test Task').exists())

    def test_delete_task_by_non_author_fails(self):
        """
        Test that non-authors cannot delete a task and receive an error message.

        Expected Behavior:
            - POST request to delete endpoint by a non-author returns 302.
            - Redirect target is the task list page.
            - Task remains in the database.
            - Error flash message 'Задачу может удалить только ее автор' is displayed.
        """
        self.client.login(username='other', password='pass123')
        response = self.client.post(self.delete_url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.list_url)
        self.assertTrue(Task.objects.filter(name='Test Task').exists())

        messages = list(get_messages(response.wsgi_request))
        self.assertIn('Задачу может удалить только ее автор', str(messages[0]))

    def test_detail_requires_login(self):
        """
        Test that unauthenticated users are redirected when accessing task details.

        Expected Behavior:
            - GET request to task detail without authentication returns 302.
            - Redirect URL contains '/login/'.
        """
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, 302)
        self.assertIn('/login/', response.url)

    def test_filter_by_status(self):
        """
        Test that tasks can be filtered by status.

        Expected Behavior:
            - Filtering by a specific status ID returns only tasks with that status.
            - Tasks with other statuses are not present in the response.
        """
        self.client.login(username='author', password='pass123')
        status2 = Status.objects.create(name='In Progress')
        Task.objects.create(name='Task 2', status=status2, author=self.author)

        response = self.client.get(self.list_url + f'?status={self.status.pk}')
        self.assertContains(response, 'Test Task')
        self.assertNotContains(response, 'Task 2')

    def test_filter_by_assignee(self):
        """
        Test that tasks can be filtered by assignee.

        Expected Behavior:
            - Filtering by a specific assignee ID returns only tasks assigned to them.
            - Tasks assigned to other users are not present in the response.
        """
        self.client.login(username='author', password='pass123')
        Task.objects.create(
            name='Task 2',
            status=self.status,
            author=self.author,
            assignee=self.other_user
        )

        response = self.client.get(self.list_url + f'?assignee={self.other_user.pk}')
        self.assertContains(response, 'Task 2')
        self.assertNotContains(response, 'Test Task')

    def test_filter_by_label(self):
        """
        Test that tasks can be filtered by label.

        Expected Behavior:
            - Filtering by a specific label ID returns only tasks with that label.
            - Tasks with other labels are not present in the response.
        """
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
        """
        Test that the 'only my tasks' filter shows only tasks authored by the current user.

        Expected Behavior:
            - Filtering with 'only_my_tasks=True' returns only tasks where the
              current user is the author.
            - Tasks authored by other users are not present in the response.
        """
        self.client.login(username='author', password='pass123')
        Task.objects.create(name='Other Task', status=self.status, author=self.other_user)

        response = self.client.get(self.list_url + '?only_my_tasks=True')
        self.assertContains(response, 'Test Task')
        self.assertNotContains(response, 'Other Task')
