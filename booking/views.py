from datetime import datetime, timedelta
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.core.cache import cache
from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic import CreateView, DeleteView, UpdateView, DetailView, ListView, FormView
from booking.models import Booking, Table, CoverImage
from .forms import ReservationForm, ContactForm
from .tasks import send_confirmation_email_task


class ReservationCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    """
    Представление для создания нового бронирования.

    Требует аутентификации пользователя и показывает сообщение об успехе после создания бронирования.
    Отправляет подтверждающее письмо с помощью Celery.

    Атрибуты:
        model (Model): Модель, связанная с представлением, в данном случае `Booking`.
        form_class (Form): Форма для создания бронирования, `ReservationForm`.
        template_name (str): Путь к шаблону для отображения страницы создания бронирования.
        success_message (str): Сообщение об успехе после создания бронирования.

    Методы:
        form_valid(form): Проверяет доступные столики и отправляет подтверждающее письмо.
        get_success_url(): Возвращает URL для перенаправления после успешного создания бронирования.
        get_available_tables(date, time, guests): Возвращает доступные столики для заданной даты и времени.
    """
    model = Booking
    form_class = ReservationForm
    template_name = 'booking/reservation_form.html'
    success_message = "Бронирование успешно создано!"

    def form_valid(self, form):
        form.instance.customer_user = self.request.user
        reservation = form.save(commit=False)
        tables = self.get_available_tables(
            form.cleaned_data.get('date'),
            form.cleaned_data.get('time'),
            form.cleaned_data.get('guests')
        )

        if tables:
            reservation.save()
            reservation.tables.set(tables)
            form.save_m2m()
            self.object = reservation

            # Отправка подтверждающего письма с помощью Celery
            send_confirmation_email_task.delay(
                "Подтверждение бронирования",
                f"""
                Здравствуйте, {reservation.name}!

                Ваше бронирование было успешно создано.
                Дата: {reservation.date}
                Время: {reservation.time}
                Количество гостей: {reservation.guests}
                Комментарии: {reservation.comments}

                Благодарим вас за бронирование.

                С уважением,
                Ваша команда
                """,
                [reservation.email]
            )

            # Отправка уведомления ресторану
            send_confirmation_email_task.delay(
                "Новое бронирование",
                f"""
                        Уважаемые коллеги,

                        Было создано новое бронирование.
                        Клиент: {reservation.name}
                        Дата: {reservation.date}
                        Время: {reservation.time}
                        Количество гостей: {reservation.guests}
                        Комментарии: {reservation.comments}

                        С уважением,
                        Ваша система бронирования
                        """,
                [settings.EMAIL_HOST_USER]
            )

            messages.success(self.request, "Бронирование успешно создано!")
            return HttpResponseRedirect(self.get_success_url())
        else:
            form.add_error(None, "Нет доступных столиков для указанного времени.")
            return self.form_invalid(form)

    def get_success_url(self):
        """
        Метод для получения URL при успешном создании бронирования.
        """
        return reverse_lazy('booking:reservation_list')

    def get_available_tables(self, date, time, guests):
        """
        Метод для получения доступных столиков на определенное время и дату с учетом количества гостей.

        Аргументы:
            date (date): Дата бронирования.
            time (time): Время бронирования.
            guests (int): Количество гостей.

        Возвращает:
            QuerySet: Доступные столики или None, если нет доступных столиков.
        """
        time = datetime.strptime(time, "%H:%M").time()
        datetime_booking = datetime.combine(date, time)
        end_time = (datetime_booking + timedelta(hours=2)).time()
        datetime_end_booking = datetime.combine(date, end_time)

        # Поиск конфликтующих бронирований
        conflicting_bookings = Booking.objects.filter(
            date=date,
            time__lt=datetime_end_booking,
            time__gte=datetime_booking
        )

        reserved_tables = conflicting_bookings.values_list('tables', flat=True)
        available_tables = Table.objects.exclude(id__in=reserved_tables)

        # Выбор столиков по количеству гостей
        tables_needed = (guests + 1) // 2
        if available_tables.count() >= tables_needed:
            return available_tables[:tables_needed]
        return None


@method_decorator(login_required, name='dispatch')
class CancelReservationView(SuccessMessageMixin, DeleteView):
    """
    Представление для отмены бронирования.

    Требует аутентификации пользователя и показывает сообщение об успехе после отмены бронирования.

    Атрибуты:
        model (Model): Модель, связанная с представлением, в данном случае `Booking`.
        template_name (str): Путь к шаблону для отображения страницы подтверждения удаления.
        success_url (str): URL, на который будет перенаправлен пользователь после успешного удаления бронирования.
        success_message (str): Сообщение об успехе после отмены бронирования.

    Методы:
        delete(request, *args, **kwargs): Удаляет бронирование и добавляет сообщение об успехе.
    """
    model = Booking
    template_name = 'booking/reservation_confirm_delete.html'
    success_url = reverse_lazy('booking:reservation_list')
    success_message = "Бронирование успешно отменено."

    def delete(self, request, *args, **kwargs):
        """
        Метод удаления бронирования с добавлением сообщения об успехе.
        """
        messages.success(self.request, self.success_message)
        return super(CancelReservationView, self).delete(request, *args, **kwargs)


class ReservationDetailView(LoginRequiredMixin, DetailView):
    """
    Представление для отображения деталей конкретного бронирования.

    Требует аутентификации пользователя.

    Атрибуты:
        model (Model): Модель, связанная с представлением, в данном случае `Booking`.
        template_name (str): Путь к шаблону для отображения страницы деталей бронирования.
        context_object_name (str): Имя контекста для объекта бронирования.
    """
    model = Booking
    template_name = 'booking/reservation_detail.html'
    context_object_name = 'reservation'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_superuser:
            context['back_url'] = reverse('booking:all_reservations')  # URL для суперпользователя
        else:
            context['back_url'] = reverse('booking:reservation_list')  # URL для обычных пользователей
        return context


@method_decorator(login_required, name='dispatch')
class ReservationListView(LoginRequiredMixin, ListView):
    """
    Представление для отображения списка бронирований текущего пользователя.

    Требует аутентификации пользователя.

    Атрибуты:
        model (Model): Модель, связанная с представлением, в данном случае `Booking`.
        template_name (str): Путь к шаблону для отображения страницы списка бронирований.
        context_object_name (str): Имя контекста для списка бронирований.

    Методы:
        get_queryset(): Возвращает список бронирований текущего пользователя, отсортированный по дате и времени.
    """
    model = Booking
    template_name = 'booking/reservation_list.html'
    context_object_name = 'reservations'

    def get_queryset(self):
        """
        Возвращает список бронирований текущего пользователя, отсортированный по дате и времени.
        """
        return Booking.objects.filter(customer_user=self.request.user).order_by('-date', '-time')


class HomeView(SuccessMessageMixin, ListView):
    """
    Представление для отображения главной страницы.

    Атрибуты:
        model (Model): Модель, связанная с представлением, в данном случае `CoverImage`.
        template_name (str): Путь к шаблону для отображения главной страницы.
        context_object_name (str): Имя контекста для объекта `CoverImage`.

    Методы:
        get_queryset(): Возвращает первый объект `CoverImage` для главной страницы.
    """
    model = CoverImage
    template_name = 'booking/home_page.html'
    context_object_name = 'cover_image'

    def get_queryset(self):
        """
        Возвращает первый объект `CoverImage`.
        """
        return CoverImage.objects.first()


class ReservationUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    """
    Представление для обновления бронирования.

    Требует аутентификации пользователя и показывает сообщение об успехе после обновления бронирования.

    Атрибуты:
        model (Model): Модель, связанная с представлением, в данном случае `Booking`.
        form_class (Form): Форма для обновления бронирования, `ReservationForm`.
        template_name (str): Путь к шаблону для отображения страницы обновления бронирования.
        success_message (str): Сообщение об успехе после обновления бронирования.

    Методы:
        form_valid(form): Сохраняет обновленное бронирование и отображает сообщение об успехе.
        get_success_url(): Возвращает URL для перенаправления после успешного обновления бронирования.
    """
    model = Booking
    form_class = ReservationForm
    template_name = 'booking/reservation_form.html'
    success_message = "Бронирование успешно обновлено!"

    def form_valid(self, form):
        """
        Метод вызывается при успешной валидации формы.
        """
        form.instance.customer_user = self.request.user
        reservation = form.save(commit=False)
        reservation.save()

        if 'tables' in form.cleaned_data:
            reservation.tables.set(form.cleaned_data['tables'])
        form.save_m2m()

        self.object = reservation
        messages.success(self.request, self.success_message)
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        """
        Метод для получения URL при успешном обновлении бронирования.
        """
        return reverse('booking:reservation_detail', kwargs={'pk': self.object.pk})


class CheckAvailableTablesView(View):
    """
    Представление для проверки доступных столиков через AJAX запрос.

    Возвращает количество доступных столиков для заданной даты, времени и количества гостей.

    Методы:
        get(request): Обрабатывает GET-запрос и возвращает количество доступных столиков в формате JSON.
    """

    def get(self, request):
        selected_date = request.GET.get('date')
        selected_time = request.GET.get('time')
        guests = request.GET.get('guests')

        available_tables_count = 0

        if selected_date and selected_time and guests:
            try:
                guests_count = int(guests)

                # Получение списка занятых столов
                reserved_tables = Booking.objects.filter(
                    date=selected_date,
                    time=selected_time
                ).values_list('tables__id', flat=True)

                # Фильтрация доступных столов по количеству гостей
                available_tables_count = Table.objects.filter(
                    capacity__gte=guests_count
                ).exclude(
                    id__in=reserved_tables
                ).count()

            except (ValueError, ValidationError):
                pass

        return JsonResponse({'count': available_tables_count})


class MyView(View):
    """
    Пример представления для демонстрации работы с кэшем.

    Методы: get(request): Обрабатывает GET-запрос, получает значение из кэша или устанавливает новое, если значение
    отсутствует.
    """

    def get(self, request):
        message = cache.get('my_key')
        if not message:
            message = 'Тест, Redis!'
            cache.set('my_key', message, timeout=60 * 15)
            print("Значения не было в кэше. Установка нового значения: " + message)
        else:
            print("Значение из кэша: " + message)
        return render(request, 'booking/test_cache.html', {'value': message})


class ContactFormView(FormView):
    """
    Представление для обработки контактной формы.

    Атрибуты:
        template_name (str): Путь к шаблону для отображения страницы контактной формы.
        form_class (Form): Форма для обработки контактных сообщений, `ContactForm`.
        success_url (str): URL для перенаправления после успешной отправки формы.

    Методы:
        form_valid(form): Обрабатывает успешную отправку формы, отправляет email и отображает сообщение об успешной
        отправке.
    """
    template_name = 'booking/contact.html'
    form_class = ContactForm
    success_url = reverse_lazy('booking:home')

    def form_valid(self, form):
        # Получение данных из формы
        name = form.cleaned_data['name']
        email = form.cleaned_data['email']
        phone = form.cleaned_data['phone']
        message = form.cleaned_data['message']

        # Составляем сообщение
        subject = 'Сообщение с контактной формы ресторана «ParkKing»'
        body = f"Имя: {name}\nEmail: {email}\nТелефон: {phone}\nСообщение:\n{message}"
        from_email = settings.DEFAULT_FROM_EMAIL
        recipient_list = ['solod-spb78@yandex.ru']  # Убедитесь, что этот адрес верный

        # Отправка email
        send_mail(subject, body, from_email, recipient_list)

        # Добавляем сообщение об успешной отправке
        messages.success(self.request, 'Ваше сообщение успешно отправлено! Мы свяжемся с вами в ближайшее время.')

        return super().form_valid(form)


@method_decorator(user_passes_test(lambda u: u.is_superuser), name='dispatch')
class AllReservationsView(ListView):
    """
    Представление для отображения всех бронирований.

    Данное представление предназначено для суперпользователей и отображает список всех
    бронирований в виде таблицы. Данные пагинируются по 10 элементов на страницу.

    Атрибуты:
    - `model` (`Booking`): Модель, данные которой будут отображены в представлении.
    - `template_name` (`str`): Имя шаблона, который будет использоваться для рендеринга страницы.
    - `context_object_name` (`str`): Имя переменной контекста, в которую будут помещены объекты модели.
    - `paginate_by` (`int`): Количество объектов модели, отображаемых на одной странице.

    Декораторы:
    - `@method_decorator(user_passes_test(lambda u: u.is_superuser), name='dispatch')`:
      Ограничивает доступ к этому представлению только суперпользователям. Если текущий пользователь
      не является суперпользователем, он будет перенаправлен на страницу входа или другую страницу,
      указанную в настройках.

    Методы:
    - `get_queryset()`:
      Возвращает queryset объектов модели `Booking`, который будет использоваться для отображения
      в представлении.
    """
    model = Booking
    template_name = 'booking/all_reservations.html'
    context_object_name = 'reservations'
    paginate_by = 10
