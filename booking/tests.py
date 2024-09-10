from django.test import TestCase, Client
from django.urls import reverse
from users.models import User
from booking.models import Booking, Table
from datetime import datetime, timedelta


class ReservationCreateViewTest(TestCase):
    """
    Тесты для проверки создания бронирований через представление ReservationCreateView.
    """

    def setUp(self):
        """
        Настройка тестового окружения.
        Создает тестового пользователя и выполняет вход в систему.
        Также создает несколько столов в базе данных для тестирования успешного бронирования.
        """
        self.client = Client()
        self.user = User.objects.create_user(
            email='testuser@example.com',
            password='12345'
        )
        self.client.login(email='testuser@example.com', password='12345')

        # Создаем 5 столов для тестирования
        for i in range(1, 6):
            Table.objects.create(number=i, capacity=4)
        self.url = reverse('booking:reservation_new')

    def test_create_reservation_success(self):
        """
        Тест успешного создания бронирования.
        Отправляет корректные данные для бронирования и проверяет,
        что после успешного бронирования происходит перенаправление,
        а запись о бронировании создается в базе данных.
        """
        valid_time = "20:00"
        data = {
            'date': (datetime.now() + timedelta(days=1)).date(),  # Устанавливаем дату на завтра
            'time': valid_time,  # Время бронирования
            'guests': 4,  # Количество гостей
            'name': 'Test Name',
            'contact_number': '1234567890',
            'phone_number': '1234567890',
            'email': 'test@example.com',
            'comments': 'No comments',
        }

        response = self.client.post(self.url, data)

        # Инициализируем переменную для хранения сообщений об ошибках формы
        form_errors = 'No form context available'

        if response.status_code != 302:
            # Выводим ошибки формы для отладки, если бронирование не удалось
            if response.context and 'form' in response.context:
                form_errors = response.context['form'].errors
            print("Form errors:", form_errors)

        self.assertEqual(response.status_code, 302,
                         msg=form_errors)  # Ожидаем перенаправление после успешного бронирования
        self.assertTrue(
            Booking.objects.filter(email='test@example.com').exists())  # Проверяем, что бронирование создано

    def test_create_reservation_no_tables_available(self):
        """
        Тест на случай, когда нет свободных столов.
        Создает существующее бронирование, которое занимает все столики,
        и пытается создать новое бронирование, которое должно завершиться неудачей.
        """
        valid_time = "20:00"
        # Создаем бронирование, чтобы занять все столики
        Booking.objects.create(
            date=(datetime.now() + timedelta(days=1)).date(),
            time=valid_time,
            guests=4,
            email='existing@example.com'
        )

        data = {
            'date': (datetime.now() + timedelta(days=1)).date(),  # Дата на завтра
            'time': valid_time,  # Время бронирования
            'guests': 4,  # Количество гостей
            'name': 'Test Name',
            'contact_number': '1234567890',
            'phone_number': '1234567890',
            'email': 'test@example.com',
            'comments': 'No comments',
        }

        response = self.client.post(self.url, data)
        form = response.context.get('form')
        self.assertTrue(form.errors)  # Ожидаем, что форма вернет ошибки из-за отсутствия свободных столов
        self.assertEqual(response.status_code, 200)  # Ошибка формы возвращает статус 200

    def test_redirect_if_not_logged_in(self):
        """
        Тест перенаправления неавторизованных пользователей.
        Проверяет, что пользователи, которые не вошли в систему,
        перенаправляются на страницу входа при попытке доступа к созданию бронирования.
        """
        self.client.logout()  # Выходим из системы
        response = self.client.get(self.url)
        self.assertRedirects(response, f'/users/login/?next={self.url}')
