from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.core import mail
from .utils import generate_token

User = get_user_model()


class UserViewsTestCase(TestCase):
    """
    Тестовый класс для проверки представлений пользователей.

    Использует `Client` для отправки запросов к представлениям и проверяет
    их правильность через различные утверждения. Также проверяет отправляемые
    электронные письма и взаимодействие с базой данных.
    """

    def setUp(self):
        """
        Устанавливает начальные условия для тестов.

        Создает пользователя и выполняет вход в систему с помощью клиента.
        """
        self.client = Client()
        self.user = User.objects.create_user(email='test@example.com', password='password123')
        self.client.login(email='test@example.com', password='password123')

    def test_register_view_get(self):
        """
        Тестирует GET-запрос к представлению регистрации.

        Проверяет, что страница регистрации загружается успешно и используется
        правильный шаблон.
        """
        response = self.client.get(reverse('users:register'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/register.html')

    def test_register_view_post(self):
        """
        Тестирует POST-запрос к представлению регистрации.

        Проверяет, что регистрация пользователя проходит успешно, происходит
        перенаправление и отправляется электронное письмо с верификацией.
        """
        data = {
            'email': 'newuser@example.com',
            'password1': 'newpassword123',
            'password2': 'newpassword123',
        }
        response = self.client.post(reverse('users:register'), data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(email='newuser@example.com').exists())
        self.assertEqual(len(mail.outbox), 1)
        self.assertIn('Верификация почты', mail.outbox[0].subject)

    def test_verify_view(self):
        """
        Тестирует представление верификации пользователя по токену.

        Проверяет, что верификация пользователя происходит успешно после
        перехода по ссылке с токеном.
        """
        token = generate_token()
        user = User.objects.create_user(email='verify@example.com', password='password123', token=token)
        response = self.client.get(reverse('users:verify_success', kwargs={'token': token}))
        user.refresh_from_db()
        self.assertEqual(response.status_code, 200)
        self.assertTrue(user.is_verified)

    def test_res_password_get(self):
        """
        Тестирует GET-запрос к представлению сброса пароля.

        Проверяет, что страница сброса пароля загружается успешно и используется
        правильный шаблон.
        """
        response = self.client.get(reverse('users:reset_password'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/reset_password.html')

    def test_res_password_post(self):
        """
        Тестирует POST-запрос к представлению сброса пароля.

        Проверяет, что сброс пароля пользователя проходит успешно, происходит
        перенаправление и отправляется электронное письмо с новым паролем.
        """
        data = {'email': 'test@example.com'}
        response = self.client.post(reverse('users:reset_password'), data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(len(mail.outbox), 1)
        self.assertIn('Смена пароля', mail.outbox[0].subject)

    def test_profile_view_get(self):
        """
        Тестирует GET-запрос к представлению профиля пользователя.

        Проверяет, что страница профиля загружается успешно и используется
        правильный шаблон.
        """
        response = self.client.get(reverse('users:profile'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/user_form.html')

    def test_login_view(self):
        """
        Тестирует GET-запрос к представлению входа пользователя.

        Проверяет, что страница входа загружается успешно и используется
        правильный шаблон.
        """
        response = self.client.get(reverse('users:login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/login.html')

    def test_delete_account_view(self):
        """
        Тестирует POST-запрос к представлению удаления аккаунта пользователя.

        Проверяет, что удаление аккаунта проходит успешно, происходит
        перенаправление, и аккаунт больше не существует в базе данных.
        """
        response = self.client.post(reverse('users:delete_account'))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(User.objects.filter(email='test@example.com').exists())

    def test_email_verification_view(self):
        """
        Тестирует GET-запрос к представлению подтверждения регистрации по электронной почте.

        Проверяет, что страница подтверждения регистрации по электронной почте
        загружается успешно и используется правильный шаблон.
        """
        response = self.client.get(reverse('users:email_verification'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/email_verification.html')
