from django.db import models
from django.contrib.auth.models import AbstractUser
from users.managers import CustomUserManager

# Параметры, которые можно применять к полям модели для разрешения пустых значений.
NULLABLE = {'blank': True, "null": True}


class User(AbstractUser):
    """
    Кастомная модель пользователя, расширяющая стандартную модель AbstractUser.

    Поля:
        - email: Уникальный адрес электронной почты пользователя. Используется как основное поле для аутентификации.
        - phone: Номер телефона пользователя (опционально).
        - avatar: Аватар пользователя, загружаемый в папку 'users/' (опционально).
        - birth_date: Дата рождения пользователя (опционально).
        - city: Город проживания пользователя (опционально).
        - country: Страна проживания пользователя (опционально).
        - is_verified: Флаг, указывающий, подтверждён ли пользователь (по умолчанию False).
        - token: Токен для верификации пользователя (опционально).
        - nickname: Уникальный никнейм пользователя (опционально).

    Атрибуты:
        - USERNAME_FIELD: Поле, используемое для аутентификации (email).
        - REQUIRED_FIELDS: Дополнительные поля, необходимые при создании суперпользователя (оставлено пустым).
        - objects: Кастомный менеджер пользователей, реализующий логику управления пользователями (CustomUserManager).

    Метаданные:
        - verbose_name: Человеко-читаемое имя модели (единственное число).
        - verbose_name_plural: Человеко-читаемое имя модели (множественное число).

    Методы:
        - __str__: Возвращает строковое представление объекта пользователя (адрес электронной почты).
    """

    # Убираем поле username, так как используется email для аутентификации
    username = None
    email = models.EmailField(unique=True, verbose_name='почта')
    phone = models.CharField(max_length=35, verbose_name='телефон', **NULLABLE)
    avatar = models.ImageField(upload_to='users/', verbose_name='аватар', **NULLABLE)
    birth_date = models.DateField(null=True, blank=True, verbose_name='Дата рождения')
    city = models.CharField(max_length=25, verbose_name="Город", **NULLABLE)
    country = models.CharField(max_length=50, verbose_name='страна', **NULLABLE)
    is_verified = models.BooleanField(default=False, verbose_name='Подтверждён')
    token = models.CharField(max_length=10, verbose_name='Токен', **NULLABLE)
    nickname = models.CharField(max_length=50, verbose_name='никнейм', unique=True, **NULLABLE)

    # Используем email в качестве поля для аутентификации вместо стандартного username
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    # Назначаем кастомный менеджер пользователей для управления моделью User
    objects = CustomUserManager()

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return f"{self.email}"
