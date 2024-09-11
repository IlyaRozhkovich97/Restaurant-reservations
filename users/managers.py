from django.contrib.auth.models import BaseUserManager


class CustomUserManager(BaseUserManager):
    """
    CustomUserManager - кастомный менеджер пользователей для работы с моделью пользователя,
    где основным идентификатором является email вместо имени пользователя.

    Этот менеджер предоставляет метод для создания суперпользователей.

    Методы:
    --------
    create_superuser(email, password=None, **extra_fields)
        Создает и возвращает суперпользователя с заданным email и паролем.
    """

    def create_superuser(self, email, password=None, **extra_fields):
        """
        Создает и возвращает суперпользователя.

        Параметры:
        ----------
        email : str
            Адрес электронной почты суперпользователя. Обязательное поле.

        password : str, optional
            Пароль для суперпользователя. По умолчанию None, но должен быть передан при создании.

        **extra_fields : dict
            Дополнительные поля, которые будут установлены у суперпользователя.

        Исключения:
        -----------
        ValueError
            Вызывается, если email не предоставлен.

        TypeError
            Вызывается, если пароль не предоставлен.

        Возвращает:
        -----------
        CustomUser
            Экземпляр суперпользователя.
        """
        if not email:
            raise ValueError('Суперпользователи должны иметь адрес электронной почты.')

        if password is None:
            raise TypeError('Суперпользователи должны иметь пароль.')

        # Создание суперпользователя
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user
