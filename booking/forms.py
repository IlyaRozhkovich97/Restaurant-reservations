from django import forms
from django.core.exceptions import ValidationError
from django.utils import timezone
from datetime import datetime, timedelta, date
from .models import Booking, Table
import re


class StyleFormMixin(forms.ModelForm):
    """
    Миксин для стилизации полей формы.

    Добавляет CSS-классы к полям формы для обеспечения единого стиля:
    - Поля типа `BooleanField` получают класс 'form-check-input'.
    - Все остальные поля получают класс 'form-control'.
    """

    def __init__(self, *args, **kwargs):
        """
        Инициализирует форму и добавляет стили к полям формы.

        :param args: Позиционные аргументы.
        :param kwargs: Именованные аргументы.
        """
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if isinstance(field, forms.BooleanField):
                field.widget.attrs['class'] = 'form-check-input'
            else:
                field.widget.attrs['class'] = 'form-control'


class ReservationForm(StyleFormMixin, forms.ModelForm):
    """
    Форма для создания бронирования.

    Позволяет пользователям выбрать дату, время, количество гостей и ввести
    контактные данные. Также выполняет валидацию даты, времени, номера телефона,
    имени и доступности столов.

    Поля:
    - `date` (`DateField`): Дата бронирования.
    - `time` (`ChoiceField`): Время бронирования.
    - `guests` (`IntegerField`): Количество гостей.
    - `name` (`CharField`): Имя клиента.
    - `email` (`EmailField`): Электронная почта клиента.
    - `phone_number` (`CharField`): Телефон клиента.
    - `comments` (`TextField`): Дополнительные комментарии.

    Метаданные:
    - `model`: Booking
    - `fields`: ['date', 'time', 'guests', 'name', 'email', 'phone_number', 'comments']
    """

    date = forms.DateField(
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        label='Дата'
    )
    time = forms.ChoiceField(
        choices=[(f"{hour:02}:{minute:02}", f"{hour:02}:{minute:02}")
                 for hour in range(24) for minute in [0, 30]],
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='Время'
    )
    guests = forms.IntegerField(
        min_value=1,
        max_value=40,
        label='Количество гостей'
    )

    class Meta:
        model = Booking
        fields = ['date', 'time', 'guests', 'name', 'email', 'phone_number', 'comments']

    def clean_date(self):
        """
        Проверяет, что дата бронирования не установлена на прошедшее время.

        :return: Дата бронирования, если она корректна.
        :raises ValidationError: Если дата в прошлом.
        """
        date_value = self.cleaned_data.get('date')
        if date_value and date_value < date.today():
            raise ValidationError("Дата не может быть в прошлом.")
        return date_value

    def clean_phone_number(self):
        """
        Проверяет, что номер телефона содержит только цифры и знак '+'.

        :return: Номер телефона, если он корректен.
        :raises ValidationError: Если номер телефона содержит недопустимые символы.
        """
        phone_number = self.cleaned_data.get('phone_number')
        if phone_number and not re.match(r'^[\d+]+$', phone_number):
            raise ValidationError("Номер телефона может содержать только цифры и знак '+'.")
        return phone_number

    def clean_name(self):
        """
        Проверяет, что имя не содержит цифры.

        :return: Имя клиента, если оно корректно.
        :raises ValidationError: Если имя содержит цифры.
        """
        name = self.cleaned_data.get('name')
        if name and re.search(r'\d', name):
            raise ValidationError("Имя не может содержать цифры.")
        return name

    def clean(self):
        """
        Выполняет дополнительную проверку после выполнения стандартной валидации.

        Проверяет доступность столов на выбранную дату и время, а также
        корректность выбранных столов для бронирования.

        :return: Очищенные данные формы.
        :raises ValidationError: Если есть конфликты с существующими бронированиями
                                 или недостаточно свободных столов.
        """
        cleaned_data = super().clean()
        date_value = cleaned_data.get('date')
        time = cleaned_data.get('time')
        guests = cleaned_data.get('guests')
        tables = cleaned_data.get('tables')

        if date_value and time:
            time = datetime.strptime(time, "%H:%M").time()
            datetime_booking = datetime.combine(date_value, time)
            end_time = (datetime_booking + timedelta(hours=2)).time()
            datetime_end_booking = datetime.combine(date_value, end_time)

            if timezone.localtime() > timezone.make_aware(datetime_booking):
                self.add_error(None, "Дата и время не могут быть в прошлом!")

            conflicting_bookings = Booking.objects.filter(
                date=date_value,
                time__lt=datetime_end_booking,
                time__gte=datetime_booking
            )

            reserved_tables = conflicting_bookings.values_list('tables', flat=True)
            available_tables = Table.objects.exclude(id__in=reserved_tables)

            tables_needed = (guests + 1) // 2
            if available_tables.count() < tables_needed:
                self.add_error(None, "Недостаточно свободных столов для указанного времени.")

            if tables and not all(table in available_tables for table in tables.all()):
                self.add_error('tables', "Все выбранные столы должны быть доступны в выбранное время.")

        return cleaned_data


class ContactForm(forms.Form):
    """
    Форма для отправки сообщений через контактную страницу.

    Позволяет пользователям ввести контактные данные и сообщение.

    Поля:
    - `name` (`CharField`): Имя отправителя.
    - `email` (`EmailField`): Электронная почта отправителя.
    - `phone` (`CharField`): Телефон отправителя.
    - `message` (`CharField`): Сообщение отправителя.
    """
    name = forms.CharField(max_length=100, required=True)
    email = forms.EmailField(required=True)
    phone = forms.CharField(max_length=20, required=True)
    message = forms.CharField(widget=forms.Textarea, required=True)
