from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
import logging

# Создаем логгер для отслеживания событий отправки электронных писем.
logger = logging.getLogger(__name__)


@shared_task
def send_confirmation_email_task(subject, message, recipient_list):
    """
    Задача Celery для отправки электронного письма.

    Отправляет электронное письмо с заданной темой и сообщением указанным
    получателям. Использует настройки Django для отправки писем.

    Параметры:
    - `subject` (`str`): Тема электронного письма.
    - `message` (`str`): Содержимое электронного письма.
    - `recipient_list` (`list` of `str`): Список адресов электронной почты получателей.

    Логгирование:
    - Записывает информацию о начале отправки письма с темой и списком получателей.

    Исключения:
    - Параметр `fail_silently=False` указывает, что исключения при отправке письма
      будут возбуждены, если возникнут проблемы.
    """

    # Логируем информацию о процессе отправки письма.
    logger.info(f"Отправка электронного письма с темой: {subject} to {recipient_list}")

    # Отправляем письмо с помощью функции send_mail из Django.
    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        recipient_list,
        fail_silently=False,
    )
