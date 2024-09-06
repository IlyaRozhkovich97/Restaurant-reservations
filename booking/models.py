from django.db import models
from django.contrib.auth import get_user_model
from datetime import timedelta
from django.core.validators import MinValueValidator, MaxValueValidator

User = get_user_model()


class Table(models.Model):
    """
    Модель стола в ресторане.

    Содержит информацию о номере стола, вместимости и связанных бронированиях.

    Поля:
    - `number` (`IntegerField`): Номер стола.
    - `capacity` (`IntegerField`): Вместимость стола. Валидация от 2 до 6.
    - `reservations` (`ManyToManyField`): Связь с моделями бронирований.

    Метаданные:
    - `verbose_name`: "Стол"
    - `verbose_name_plural`: "Столы"
    - `ordering`: ['number']

    Методы:
    - `__str__`: Возвращает строковое представление стола в формате:
      'Стол {номер} на {вместимость} гостей'.
    """

    objects = None
    number = models.IntegerField(verbose_name="Номер стола")
    capacity = models.IntegerField(
        verbose_name="Вместимость",
        validators=[MinValueValidator(2), MaxValueValidator(6)],
        default=2
    )
    reservations = models.ManyToManyField(
        'Booking',
        related_name='related_tables',
        blank=True,
        verbose_name="Бронирования"
    )

    def __str__(self):
        return f'Стол {self.number} на {self.capacity} гостей'

    class Meta:
        verbose_name = "Стол"
        verbose_name_plural = "Столы"
        ordering = ['number']


class Booking(models.Model):
    """
    Модель бронирования стола в ресторане.

    Содержит информацию о дате, времени, количестве гостей, контактных данных
    клиента, связанных столах и продолжительности бронирования.

    Поля:
    - `id` (`AutoField`): Уникальный идентификатор бронирования.
    - `date` (`DateField`): Дата бронирования.
    - `time` (`TimeField`): Время бронирования.
    - `guests` (`IntegerField`): Количество гостей.
    - `name` (`CharField`): Имя клиента.
    - `email` (`EmailField`): Электронная почта клиента.
    - `phone_number` (`CharField`): Телефон клиента.
    - `comments` (`TextField`): Дополнительные комментарии.
    - `tables` (`ManyToManyField`): Связь с моделями столов.
    - `customer_user` (`ForeignKey`): Связь с пользователем, сделавшим бронирование.
    - `duration` (`DurationField`): Продолжительность бронирования.

    Метаданные:
    - `verbose_name`: "Бронирование"
    - `verbose_name_plural`: "Бронирования"

    Методы:
    - `__str__`: Возвращает строковое представление бронирования в формате:
      'Бронирование {идентификатор} - {имя клиента}'.
    """

    objects = None
    id = models.AutoField(primary_key=True)
    date = models.DateField(verbose_name="Дата")
    time = models.TimeField(verbose_name="Время")
    guests = models.IntegerField(verbose_name="Количество гостей")
    name = models.CharField(max_length=50, verbose_name="Имя")
    email = models.EmailField(max_length=254, verbose_name="Электронная почта")
    phone_number = models.CharField(max_length=20, verbose_name="Телефон")
    comments = models.TextField(blank=True, null=True, verbose_name="Комментарии")
    tables = models.ManyToManyField(
        'Table',
        related_name='related_reservations',
        blank=True,
        verbose_name="Столы"
    )
    customer_user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name="Пользователь"
    )
    duration = models.DurationField(default=timedelta(hours=2), verbose_name="Продолжительность")

    class Meta:
        verbose_name = "Бронирование"
        verbose_name_plural = "Бронирования"

    def __str__(self):
        return f"Бронирование {self.id} - {self.name}"


class CoverImage(models.Model):
    """
    Модель изображения обложки.

    Содержит информацию о заголовке и изображении обложки.

    Поля:
    - `title` (`CharField`): Название изображения.
    - `image` (`ImageField`): Изображение, загружаемое в папку 'covers/'.

    Метаданные:
    - `verbose_name`: "Обложка"
    - `verbose_name_plural`: "Обложки"

    Методы:
    - `__str__`: Возвращает строковое представление изображения в формате:
      'Название изображения'.
    """

    title = models.CharField(max_length=100, verbose_name="Название")
    image = models.ImageField(upload_to='covers/', verbose_name="Изображение")

    class Meta:
        verbose_name = "Обложка"
        verbose_name_plural = "Обложки"

    def __str__(self):
        return self.title
