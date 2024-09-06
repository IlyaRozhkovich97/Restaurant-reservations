from django.core.cache import cache
from booking.models import Table, Booking, CoverImage
from config.settings import CACHE_ENABLED


def get_tables_from_cache():
    """
    Получение списка столов с использованием кэширования.

    Проверяет, включено ли кэширование. Если кэширование отключено, выполняется запрос к базе данных для получения
    всех столов. Если кэширование включено, сначала пытается извлечь данные из кэша. Если данные не найдены в кэше,
    выполняется запрос к базе данных, и результат сохраняется в кэше.

    Возвращаемое значение:
        QuerySet: Список всех столов, полученный из кэша или базы данных.
    """
    if not CACHE_ENABLED:
        return Table.objects.all()
    else:
        key = 'tables_list'
        tables = cache.get(key)
        if tables is not None:
            return tables
        else:
            tables = Table.objects.all()
            cache.set(key, tables)
            return tables


def get_bookings_from_cache():
    """
    Получение списка бронирований с использованием кэширования.

    Проверяет, включено ли кэширование. Если кэширование отключено, выполняется запрос к базе данных для получения
     всех бронирований. Если кэширование включено, сначала пытается извлечь данные из кэша. Если данные не найдены
     в кэше, выполняется запрос к базе данных, и результат сохраняется в кэше.

    Возвращаемое значение:
        QuerySet: Список всех бронирований, полученный из кэша или базы данных.
    """
    if not CACHE_ENABLED:
        return Booking.objects.all()
    else:
        key = 'bookings_list'
        bookings = cache.get(key)
        if bookings is not None:
            return bookings
        else:
            bookings = Booking.objects.all()
            cache.set(key, bookings)
            return bookings


def get_cover_images_from_cache():
    """
    Получение списка обложек с использованием кэширования.

    Проверяет, включено ли кэширование. Если кэширование отключено, выполняется запрос к базе данных для
    получения всех обложек. Если кэширование включено, сначала пытается извлечь данные из кэша. Если данные
    не найдены в кэше, выполняется запрос к базе данных, и результат сохраняется в кэше.

    Возвращаемое значение:
        QuerySet: Список всех обложек, полученный из кэша или базы данных.
    """
    if not CACHE_ENABLED:
        return CoverImage.objects.all()
    else:
        key = 'cover_images_list'
        cover_images = cache.get(key)
        if cover_images is not None:
            return cover_images
        else:
            cover_images = CoverImage.objects.all()
            cache.set(key, cover_images)
            return cover_images
