from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from django.contrib.messages import get_messages
from django.utils import translation


class UserRegistrationTest(TestCase):
    def setUp(self):
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
        response = self.client.get(self.register_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/create.html')

    def test_user_registration_success(self):
        response = self.client.post(self.register_url, self.user_data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('login'))
        
        # Проверка, что пользователь создан
        self.assertTrue(User.objects.filter(username='johndoe').exists())
        
        # Проверка flash-сообщения (английское, так как в тестах язык по умолчанию)
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertIn('successfully registered', str(messages[0]))

    def test_user_registration_with_existing_username(self):
        User.objects.create_user(
            username='johndoe',
            password='existingpassword'
        )
        response = self.client.post(self.register_url, self.user_data)
        self.assertEqual(response.status_code, 200)
        form = response.context['form']
        self.assertTrue(form.has_error('username'))

    def test_user_registration_with_password_mismatch(self):
        data = self.user_data.copy()
        data['password2'] = 'differentpassword'
        response = self.client.post(self.register_url, data)
        self.assertEqual(response.status_code, 200)
        form = response.context['form']
        self.assertTrue(form.has_error('password2'))


class UserLoginTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.login_url = reverse('login')
        self.user = User.objects.create_user(
            username='testuser',
            password='testpassword123',
            first_name='Test',
            last_name='User'
        )

    def test_login_page_accessible(self):
        response = self.client.get(self.login_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/login.html')

    def test_login_success(self):
        response = self.client.post(self.login_url, {
            'username': 'testuser',
            'password': 'testpassword123',
        })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('home'))
        
        # Проверка, что пользователь аутентифицирован
        self.assertTrue(response.wsgi_request.user.is_authenticated)
        
        # Проверка flash-сообщения
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertIn('logged in', str(messages[0]))

    def test_login_with_invalid_credentials(self):
        response = self.client.post(self.login_url, {
            'username': 'testuser',
            'password': 'wrongpassword',
        })
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.wsgi_request.user.is_authenticated)


class UserLogoutTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.logout_url = reverse('logout')
        self.user = User.objects.create_user(
            username='testuser',
            password='testpassword123'
        )
        self.client.login(username='testuser', password='testpassword123')

    def test_logout_success(self):
        response = self.client.post(self.logout_url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('home'))
        
        # Проверка, что пользователь вышел
        response = self.client.get(reverse('home'))
        self.assertFalse(response.wsgi_request.user.is_authenticated)


class UserListViewTest(TestCase):
    def setUp(self):
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
        response = self.client.get(self.users_list_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/list.html')

    def test_users_list_shows_all_users(self):
        response = self.client.get(self.users_list_url)
        self.assertContains(response, 'user1')
        self.assertContains(response, 'user2')
        self.assertContains(response, 'User')
        self.assertContains(response, 'One')
        self.assertContains(response, 'Two')


class UserUpdateViewTest(TestCase):
    def setUp(self):
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
        self.client.login(username='testuser', password='testpassword123')
        response = self.client.post(self.update_url, {
            'first_name': 'Updated',
            'last_name': 'Name',
            'username': 'testuser',
        })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('users_list'))
        
        # Проверка, что данные обновлены
        self.user.refresh_from_db()
        self.assertEqual(self.user.first_name, 'Updated')
        self.assertEqual(self.user.last_name, 'Name')
        
        # Проверка flash-сообщения
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertIn('successfully updated', str(messages[0]))

    def test_user_cannot_update_other_user(self):
        self.client.login(username='testuser', password='testpassword123')
        response = self.client.post(self.other_user_update_url, {
            'first_name': 'Hacked',
            'last_name': 'Name',
            'username': 'otheruser',
        })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('users_list'))
        
        # Проверка, что данные НЕ обновлены
        self.other_user.refresh_from_db()
        self.assertEqual(self.other_user.first_name, 'Other')
        
        # Проверка flash-сообщения об ошибке
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertIn('permission', str(messages[0]))

    def test_unauthenticated_user_cannot_update(self):
        response = self.client.get(self.update_url)
        self.assertEqual(response.status_code, 302)
        self.assertIn('/login/', response.url)


class UserDeleteViewTest(TestCase):
    def setUp(self):
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
        self.client.login(username='testuser', password='testpassword123')
        response = self.client.post(self.delete_url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('users_list'))
        
        # Проверка, что пользователь удален
        self.assertFalse(User.objects.filter(username='testuser').exists())
        
        # Проверка flash-сообщения
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertIn('successfully deleted', str(messages[0]))

    def test_user_cannot_delete_other_user(self):
        self.client.login(username='testuser', password='testpassword123')
        response = self.client.post(self.other_user_delete_url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('users_list'))
        
        # Проверка, что пользователь НЕ удален
        self.assertTrue(User.objects.filter(username='otheruser').exists())
        
        # Проверка flash-сообщения об ошибке
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertIn('permission', str(messages[0]))

    def test_unauthenticated_user_cannot_delete(self):
        response = self.client.post(self.delete_url)
        self.assertEqual(response.status_code, 302)
        self.assertIn('/login/', response.url)
