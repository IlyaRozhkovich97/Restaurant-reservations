from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, UpdateView
from django.contrib import messages
from .forms import UserRegisterForm, UserProfileForm, CustomAuthenticationForm
from .models import User
from .utils import generate_token, generate_password
from django.contrib.auth.views import LoginView


# Класс для регистрации новых пользователей
class RegisterView(CreateView):
    """
    Представление для регистрации новых пользователей.

    Использует форму `UserRegisterForm` для сбора данных пользователя и
    создаёт нового пользователя с уникальным токеном для верификации.
    После регистрации отправляется письмо с ссылкой для подтверждения
    электронной почты.

    Атрибуты:
        model (Model): Модель, связанная с представлением, в данном случае `User`.
        form_class (Form): Форма для регистрации пользователя, `UserRegisterForm`.
        template_name (str): Путь к шаблону для отображения страницы регистрации.
        success_url (str): URL, на который будет перенаправлен пользователь после успешной регистрации.
    """
    model = User
    form_class = UserRegisterForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('users:login')

    def form_valid(self, form):
        """
        Проверяет форму на валидность, добавляет токен и отправляет письмо с подтверждением.

        Аргументы:
            form (Form): Валидная форма `UserRegisterForm`.

        Возвращает:
            HttpResponseRedirect: Перенаправление на `success_url` после успешной регистрации.
        """
        token = generate_token()
        form.instance.token = token
        user = form.save()
        user.email_user(
            subject='Верификация почты',
            message=f'Поздравляем с регистрацией на iStore \n'
                    f'Для подтверждения регистрации перейдите по ссылке: \n'
                    f'http://127.0.0.1:8000/users/confirm/{user.token} \n'
                    f'Если вы не причастны к регистрации игнорируйте это письмо.'
        )
        return super().form_valid(form)


# Функция для верификации пользователя по токену
def verify_view(request, token):
    """
    Функция для верификации пользователя по уникальному токену.

    Аргументы:
        request (HttpRequest): Запрос от клиента.
        token (str): Уникальный токен для верификации.

    Возвращает:
        HttpResponse: Рендерит страницу с подтверждением верификации.
    """
    user = get_object_or_404(User, token=token)
    user.is_verified = True
    user.save()
    return render(request, 'users/verify.html')


# Функция для сброса пароля
def res_password(request):
    """
    Функция для сброса пароля пользователя. Отправляет новый пароль на
    электронную почту пользователя и обновляет пароль в системе.

    Аргументы:
        request (HttpRequest): Запрос от клиента с методом POST.

    Возвращает:
        HttpResponseRedirect: Перенаправление на страницу сброса пароля после обработки запроса.
        HttpResponse: Рендерит страницу сброса пароля при GET запросе.
    """
    if request.method == 'POST':
        email = request.POST.get('email')
        user = User.objects.filter(email=email).first()
        if user:
            new_password = generate_password()
            user.email_user(
                subject='Смена пароля',
                message=f'Ваш новый пароль {new_password}'
            )
            user.set_password(new_password)
            user.save()
        else:
            messages.error(request, 'Пользователь не найден.')
        return redirect(reverse('users:reset_password'))
    return render(request, 'users/reset_password.html')


# Класс для обновления профиля пользователя
class ProfileView(UpdateView):
    """
    Представление для обновления профиля пользователя.

    Использует форму `UserProfileForm` для обновления информации профиля
    текущего пользователя. Перенаправляет на страницу профиля после успешного обновления.

    Атрибуты:
        model (Model): Модель, связанная с представлением, в данном случае `User`.
        form_class (Form): Форма для обновления профиля пользователя, `UserProfileForm`.
        success_url (str): URL, на который будет перенаправлен пользователь после успешного обновления профиля.
    """
    model = User
    form_class = UserProfileForm
    success_url = reverse_lazy('users:profile')

    def get_object(self, queryset=None):
        """
        Возвращает объект пользователя для обновления.

        Аргументы:
            queryset (QuerySet, optional): Опциональный QuerySet для фильтрации объектов.

        Возвращает:
            User: Текущий пользователь.
        """
        return self.request.user


# Класс для обработки входа пользователя в систему
class CustomLoginView(LoginView):
    """
    Кастомизированное представление для входа пользователя в систему.

    Использует форму `CustomAuthenticationForm` для аутентификации и
    отображает кастомизированный шаблон для входа.

    Атрибуты:
        form_class (Form): Форма для аутентификации, `CustomAuthenticationForm`.
        template_name (str): Путь к шаблону для отображения страницы входа.
    """
    form_class = CustomAuthenticationForm
    template_name = 'users/login.html'
