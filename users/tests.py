"""
Tests for user registration, authentication, profile updates, and CRUD operations.
"""
from django.contrib.auth.models import User
from django.contrib.messages import get_messages
from django.test import Client, TestCase
from django.urls import reverse


class UserRegistrationTest(TestCase):
    """
    Test suite for user registration functionality.
    """

    def setUp(self):
        """
        Set up test client and registration data.
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
        Registration page should be accessible and use the correct template.
        """
        response = self.client.get(self.register_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/create.html')

    def test_user_registration_success(self):
        """
        Successful registration should create a user and redirect to login.
        """
        response = self.client.post(self.register_url, self.user_data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('login'))

        self.assertTrue(User.objects.filter(username='johndoe').exists())

        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertIn('successfully registered', str(messages[0]))

    def test_user_registration_with_existing_username(self):
        """
        Registration with an existing username should fail with a form error.
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
        Registration with mismatched passwords should fail with a form error.
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
    """

    def setUp(self):
        """
        Set up test client and a test user.
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
        Login page should be accessible and use the correct template.
        """
        response = self.client.get(self.login_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/login.html')

    def test_login_success(self):
        """
        Successful login should authenticate the user and redirect to home.
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
        self.assertIn('logged in', str(messages[0]))

    def test_login_with_invalid_credentials(self):
        """
        Login with invalid credentials should fail and keep the user unauthenticated.
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
    """

    def setUp(self):
        """
        Set up test client and log in a test user.
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
        Successful logout should deauthenticate the user and redirect to home.
        """
        response = self.client.post(self.logout_url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('home'))

        response = self.client.get(reverse('home'))
        self.assertFalse(response.wsgi_request.user.is_authenticated)


class UserListViewTest(TestCase):
    """
    Test suite for the user list view.
    """

    def setUp(self):
        """
        Set up test client and test users.
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
        User list should be accessible without authentication.
        """
        response = self.client.get(self.users_list_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/list.html')

    def test_users_list_shows_all_users(self):
        """
        User list should display all users with their details.
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
    """

    def setUp(self):
        """
        Set up test client and test users.
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
        Users should be able to update their own profile.
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
        self.assertIn('successfully updated', str(messages[0]))

    def test_user_cannot_update_other_user(self):
        """
        Users should not be able to update other users' profiles.
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
        self.assertIn('permission', str(messages[0]))

    def test_unauthenticated_user_cannot_update(self):
        """
        Unauthenticated users should be redirected to login when accessing update page.
        """
        response = self.client.get(self.update_url)
        self.assertEqual(response.status_code, 302)
        self.assertIn('/login/', response.url)


class UserDeleteViewTest(TestCase):
    """
    Test suite for user deletion functionality.
    """

    def setUp(self):
        """
        Set up test client and test users.
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
        Users should be able to delete their own account.
        """
        self.client.login(username='testuser', password='testpassword123')
        response = self.client.post(self.delete_url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('users_list'))

        self.assertFalse(User.objects.filter(username='testuser').exists())

        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertIn('successfully deleted', str(messages[0]))

    def test_user_cannot_delete_other_user(self):
        """
        Users should not be able to delete other users' accounts.
        """
        self.client.login(username='testuser', password='testpassword123')
        response = self.client.post(self.other_user_delete_url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('users_list'))

        self.assertTrue(User.objects.filter(username='otheruser').exists())

        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertIn('permission', str(messages[0]))

    def test_unauthenticated_user_cannot_delete(self):
        """
        Unauthenticated users should be redirected to login when accessing delete page.
        """
        response = self.client.post(self.delete_url)
        self.assertEqual(response.status_code, 302)
        self.assertIn('/login/', response.url)
