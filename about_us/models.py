from django.db import models


class RestaurantHistory(models.Model):
    """
    Модель для хранения информации о истории ресторана.

    Атрибуты:
        title (CharField): Название истории ресторана.
        description (TextField): Подробное описание истории ресторана.
        image (ImageField): Изображение, связанное с историей ресторана.
        created_at (DateTimeField): Дата и время создания записи.
        is_published (BooleanField): Флаг, указывающий, опубликована ли история.

    Класс Meta:
        verbose_name (str): Человеко-читаемое название модели в единственном числе.
        verbose_name_plural (str): Человеко-читаемое название модели во множественном числе.

    Методы:
        __str__(): Возвращает название истории ресторана.
    """
    objects = None
    title = models.CharField(max_length=255, default='История ресторана', verbose_name='Название')
    description = models.TextField(verbose_name='Описание')
    image = models.ImageField(upload_to='history_images/', blank=True, null=True, verbose_name='Изображение')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    is_published = models.BooleanField(default=True, verbose_name='Опубликовано')

    class Meta:
        verbose_name = 'История ресторана'
        verbose_name_plural = 'Истории ресторанов'

    def __str__(self):
        return self.title


class MissionAndValues(models.Model):
    """
    Модель для хранения информации о миссии и ценностях ресторана.

    Атрибуты:
        mission (TextField): Миссия ресторана.
        values (TextField): Ценности ресторана.
        created_at (DateTimeField): Дата и время создания записи.
        is_published (BooleanField): Флаг, указывающий, опубликованы ли миссия и ценности.

    Класс Meta:
        verbose_name (str): Человеко-читаемое название модели в единственном числе.
        verbose_name_plural (str): Человеко-читаемое название модели во множественном числе.

    Методы:
        __str__(): Возвращает строку 'Миссия и ценности'.
    """
    objects = None
    mission = models.TextField(verbose_name='Миссия')
    values = models.TextField(verbose_name='Ценности')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    is_published = models.BooleanField(default=True, verbose_name='Опубликовано')

    class Meta:
        verbose_name = 'Миссия и ценности'
        verbose_name_plural = 'Миссии и ценности'

    def __str__(self):
        return 'Миссия и ценности'


class TeamMember(models.Model):
    """
    Модель для хранения информации о членах команды ресторана.

    Атрибуты:
        name (CharField): Имя члена команды.
        position (CharField): Должность члена команды.
        description (TextField): Описание члена команды.
        photo (ImageField): Фотография члена команды.
        created_at (DateTimeField): Дата и время создания записи.

    Класс Meta:
        verbose_name (str): Человеко-читаемое название модели в единственном числе.
        verbose_name_plural (str): Человеко-читаемое название модели во множественном числе.

    Методы:
        __str__(): Возвращает имя члена команды.
    """
    objects = None
    name = models.CharField(max_length=255, verbose_name='Имя')
    position = models.CharField(max_length=255, verbose_name='Должность')
    description = models.TextField(verbose_name='Описание')
    photo = models.ImageField(upload_to='team_photos/', blank=True, null=True, verbose_name='Фотография')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')

    class Meta:
        verbose_name = 'Член команды'
        verbose_name_plural = 'Члены команды'

    def __str__(self):
        return self.name
