"""
Tests for user registration, authentication, profile updates, and CRUD operations.

This module contains comprehensive test cases for verifying the complete
user lifecycle, including registration, login, logout, profile updates,
and account deletion. It ensures that access controls are properly enforced
and that appropriate feedback is provided to users via flash messages.
"""
from django.contrib.auth.models import User
from django.contrib.messages import get_messages
from django.test import Client, TestCase
from django.urls import reverse


class UserRegistrationTest(TestCase):
    """
    Test suite for user registration functionality.

    Verifies that the registration page is accessible, new users can be
    successfully created with valid data, and appropriate validation errors
    are displayed for invalid data (e.g., existing username, mismatched passwords).
    """

    def setUp(self):
        """
        Set up test client and registration data.

        Initializes the Django test client and defines a dictionary of
        valid user data to be used across registration tests.
        """
        self.client = Client()
        self.register_url = reverse('users_create')
        self.user_data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'username': 'johndoe',
            'password1': 'testpassword123',
            'password2': 'testpassword123',
        }

    def test_registration_page_accessible(self):
        """
        Test that the registration page is accessible and uses the correct template.

        Expected Behavior:
            - GET request to registration URL returns 200 OK.
            - The 'users/create.html' template is used to render the response.
        """
        response = self.client.get(self.register_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/create.html')

    def test_user_registration_success(self):
        """
        Test that successful registration creates a user and redirects to login.

        Expected Behavior:
            - POST request with valid user data returns 302 redirect.
            - Redirect target is the login page.
            - A new User object is created in the database.
            - A success flash message is displayed.
        """
        response = self.client.post(self.register_url, self.user_data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('login'))

        self.assertTrue(User.objects.filter(username='johndoe').exists())

        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertIn('успешно зарегистрирован', str(messages[0]))

    def test_user_registration_with_existing_username(self):
        """
        Test that registration with an existing username fails with a form error.

        Expected Behavior:
            - POST request with a username that already exists returns 200 OK.
            - The form contains a validation error for the 'username' field.
            - No new user is created.
        """
        User.objects.create_user(
            username='johndoe',
            password='existingpassword'
        )
        response = self.client.post(self.register_url, self.user_data)
        self.assertEqual(response.status_code, 200)
        form = response.context['form']
        self.assertTrue(form.has_error('username'))

    def test_user_registration_with_password_mismatch(self):
        """
        Test that registration with mismatched passwords fails with a form error.

        Expected Behavior:
            - POST request with mismatched 'password1' and 'password2' returns 200 OK.
            - The form contains a validation error for the 'password2' field.
            - No new user is created.
        """
        data = self.user_data.copy()
        data['password2'] = 'differentpassword'
        response = self.client.post(self.register_url, data)
        self.assertEqual(response.status_code, 200)
        form = response.context['form']
        self.assertTrue(form.has_error('password2'))


class UserLoginTest(TestCase):
    """
    Test suite for user login functionality.

    Verifies that the login page is accessible, users can successfully
    authenticate with valid credentials, and invalid credentials are rejected.
    """

    def setUp(self):
        """
        Set up test client and a test user.

        Initializes the Django test client and creates a test user
        with known credentials for login testing.
        """
        self.client = Client()
        self.login_url = reverse('login')
        self.user = User.objects.create_user(
            username='testuser',
            password='testpassword123',
            first_name='Test',
            last_name='User'
        )

    def test_login_page_accessible(self):
        """
        Test that the login page is accessible and uses the correct template.

        Expected Behavior:
            - GET request to login URL returns 200 OK.
            - The 'users/login.html' template is used to render the response.
        """
        response = self.client.get(self.login_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/login.html')

    def test_login_success(self):
        """
        Test that successful login authenticates the user and redirects to home.

        Expected Behavior:
            - POST request with valid credentials returns 302 redirect.
            - Redirect target is the home page.
            - The user is authenticated in the request object.
            - A success flash message is displayed.
        """
        response = self.client.post(self.login_url, {
            'username': 'testuser',
            'password': 'testpassword123',
        })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('home'))

        self.assertTrue(response.wsgi_request.user.is_authenticated)

        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertIn('вошли в систему', str(messages[0]))

    def test_login_with_invalid_credentials(self):
        """
        Test that login with invalid credentials fails and keeps the user unauthenticated.

        Expected Behavior:
            - POST request with incorrect password returns 200 OK (re-renders form).
            - The user remains unauthenticated in the request object.
        """
        response = self.client.post(self.login_url, {
            'username': 'testuser',
            'password': 'wrongpassword',
        })
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.wsgi_request.user.is_authenticated)


class UserLogoutTest(TestCase):
    """
    Test suite for user logout functionality.

    Verifies that authenticated users can successfully log out and are
    redirected to the home page, with their session cleared.
    """

    def setUp(self):
        """
        Set up test client and log in a test user.

        Initializes the Django test client, creates a test user, and
        authenticates the client with this user's credentials.
        """
        self.client = Client()
        self.logout_url = reverse('logout')
        self.user = User.objects.create_user(
            username='testuser',
            password='testpassword123'
        )
        self.client.login(username='testuser', password='testpassword123')

    def test_logout_success(self):
        """
        Test that successful logout deauthenticates the user and redirects to home.

        Expected Behavior:
            - POST request to logout URL returns 302 redirect.
            - Redirect target is the home page.
            - Subsequent requests show the user as unauthenticated.
        """
        response = self.client.post(self.logout_url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('home'))

        response = self.client.get(reverse('home'))
        self.assertFalse(response.wsgi_request.user.is_authenticated)


class UserListViewTest(TestCase):
    """
    Test suite for the user list view.

    Verifies that the user list page is publicly accessible and correctly
    displays the details of all registered users.
    """

    def setUp(self):
        """
        Set up test client and test users.

        Initializes the Django test client and creates multiple test users
        to verify that the list view displays all of them correctly.
        """
        self.client = Client()
        self.users_list_url = reverse('users_list')
        self.user1 = User.objects.create_user(
            username='user1',
            password='password1',
            first_name='User',
            last_name='One'
        )
        self.user2 = User.objects.create_user(
            username='user2',
            password='password2',
            first_name='User',
            last_name='Two'
        )

    def test_users_list_accessible_without_auth(self):
        """
        Test that the user list is accessible without authentication.

        Expected Behavior:
            - GET request to users list URL returns 200 OK.
            - The 'users/list.html' template is used to render the response.
        """
        response = self.client.get(self.users_list_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/list.html')

    def test_users_list_shows_all_users(self):
        """
        Test that the user list displays all users with their details.

        Expected Behavior:
            - GET request to users list URL returns 200 OK.
            - The response content contains the usernames, first names,
              and last names of all created test users.
        """
        response = self.client.get(self.users_list_url)
        self.assertContains(response, 'user1')
        self.assertContains(response, 'user2')
        self.assertContains(response, 'User')
        self.assertContains(response, 'One')
        self.assertContains(response, 'Two')


class UserUpdateViewTest(TestCase):
    """
    Test suite for user profile update functionality.

    Verifies that users can update their own profiles, cannot update other
    users' profiles, and unauthenticated users are redirected to login.
    """

    def setUp(self):
        """
        Set up test client and test users.

        Initializes the Django test client and creates two test users:
        one for testing self-updates and another for testing unauthorized
        update attempts.
        """
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpassword123',
            first_name='Test',
            last_name='User'
        )
        self.other_user = User.objects.create_user(
            username='otheruser',
            password='otherpassword123',
            first_name='Other',
            last_name='User'
        )
        self.update_url = reverse('users_update', kwargs={'pk': self.user.pk})
        self.other_user_update_url = reverse('users_update', kwargs={'pk': self.other_user.pk})

    def test_user_can_update_own_profile(self):
        """
        Test that users can successfully update their own profile.

        Expected Behavior:
            - POST request with valid update data returns 302 redirect.
            - Redirect target is the users list page.
            - The user's first and last names are updated in the database.
            - A success flash message is displayed.
        """
        self.client.login(username='testuser', password='testpassword123')
        response = self.client.post(self.update_url, {
            'first_name': 'Updated',
            'last_name': 'Name',
            'username': 'testuser',
        })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('users_list'))

        self.user.refresh_from_db()
        self.assertEqual(self.user.first_name, 'Updated')
        self.assertEqual(self.user.last_name, 'Name')

        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertIn('успешно обновлен', str(messages[0]))

    def test_user_cannot_update_other_user(self):
        """
        Test that users cannot update other users' profiles.

        Expected Behavior:
            - POST request to another user's update URL returns 302 redirect.
            - Redirect target is the users list page.
            - The other user's data remains unchanged in the database.
            - An error flash message indicating lack of permissions is displayed.
        """
        self.client.login(username='testuser', password='testpassword123')
        response = self.client.post(self.other_user_update_url, {
            'first_name': 'Hacked',
            'last_name': 'Name',
            'username': 'otheruser',
        })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('users_list'))

        self.other_user.refresh_from_db()
        self.assertEqual(self.other_user.first_name, 'Other')

        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertIn('нет прав', str(messages[0]))

    def test_unauthenticated_user_cannot_update(self):
        """
        Test that unauthenticated users are redirected to login when accessing the update page.

        Expected Behavior:
            - GET request to update URL without authentication returns 302 redirect.
            - Redirect URL contains '/login/'.
        """
        response = self.client.get(self.update_url)
        self.assertEqual(response.status_code, 302)
        self.assertIn('/login/', response.url)


class UserDeleteViewTest(TestCase):
    """
    Test suite for user deletion functionality.

    Verifies that users can delete their own accounts, cannot delete other
    users' accounts, and unauthenticated users are redirected to login.
    """

    def setUp(self):
        """
        Set up test client and test users.

        Initializes the Django test client and creates two test users:
        one for testing self-deletion and another for testing unauthorized
        deletion attempts.
        """
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpassword123'
        )
        self.other_user = User.objects.create_user(
            username='otheruser',
            password='otherpassword123'
        )
        self.delete_url = reverse('users_delete', kwargs={'pk': self.user.pk})
        self.other_user_delete_url = reverse('users_delete', kwargs={'pk': self.other_user.pk})

    def test_user_can_delete_own_account(self):
        """
        Test that users can successfully delete their own account.

        Expected Behavior:
            - POST request to delete URL returns 302 redirect.
            - Redirect target is the users list page.
            - The user is removed from the database.
            - A success flash message is displayed.
        """
        self.client.login(username='testuser', password='testpassword123')
        response = self.client.post(self.delete_url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('users_list'))

        self.assertFalse(User.objects.filter(username='testuser').exists())

        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertIn('успешно удален', str(messages[0]))

    def test_user_cannot_delete_other_user(self):
        """
        Test that users cannot delete other users' accounts.

        Expected Behavior:
            - POST request to another user's delete URL returns 302 redirect.
            - Redirect target is the users list page.
            - The other user remains in the database.
            - An error flash message indicating lack of permissions is displayed.
        """
        self.client.login(username='testuser', password='testpassword123')
        response = self.client.post(self.other_user_delete_url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('users_list'))

        self.assertTrue(User.objects.filter(username='otheruser').exists())

        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertIn('нет прав', str(messages[0]))

    def test_unauthenticated_user_cannot_delete(self):
        """
        Test that unauthenticated users are redirected to login when accessing the delete page.

        Expected Behavior:
            - POST request to delete URL without authentication returns 302 redirect.
            - Redirect URL contains '/login/'.
        """
        response = self.client.post(self.delete_url)
        self.assertEqual(response.status_code, 302)
        self.assertIn('/login/', response.url)
