from django.contrib import admin
from .models import Table, Booking, CoverImage

# Регистрируем модель Table в админ-панели.
# Эта модель будет доступна для просмотра и редактирования в административном интерфейсе Django.
admin.site.register(Table)

# Регистрируем модель Booking в админ-панели.
# Эта модель будет доступна для просмотра и редактирования в административном интерфейсе Django.
admin.site.register(Booking)


@admin.register(CoverImage)
class CoverImageAdmin(admin.ModelAdmin):
    """
    Административный интерфейс для модели CoverImage.

    Класс CoverImageAdmin настраивает отображение модели CoverImage в административном интерфейсе Django.
    """

    # Поля, которые будут отображаться в списке объектов модели CoverImage
    list_display = ['title', 'image']
