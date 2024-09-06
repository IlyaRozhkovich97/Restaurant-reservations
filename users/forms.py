from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from users.models import User
from django.forms import ModelForm, BooleanField
from django import forms
from django.contrib.auth.forms import AuthenticationForm


class StyleFormMixin(ModelForm):
    """
    Миксин для стилизации форм.

    Добавляет классы CSS к виджетам формы для обеспечения единообразного внешнего вида.
    Применяет класс 'form-control' ко всем полям, кроме `BooleanField`, для которых используется 'form-check-input'.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if isinstance(field, BooleanField):
                field.widget.attrs['class'] = 'form-check-input'
            else:
                field.widget.attrs['class'] = 'form-control'


class UserRegisterForm(UserCreationForm, StyleFormMixin):
    """
    Форма регистрации нового пользователя.

    Наследует от `UserCreationForm` и `StyleFormMixin`. Использует поля модели `User` для регистрации пользователя.

    Поля:
        email (EmailField): Адрес электронной почты пользователя.
        first_name (CharField): Имя пользователя.
        last_name (CharField): Фамилия пользователя.
        phone (CharField): Телефонный номер пользователя.
        city (CharField): Город проживания пользователя.
        country (CharField): Страна проживания пользователя.
        avatar (ImageField): Аватар пользователя.
        password1 (CharField): Пароль пользователя (ввод при регистрации).
        password2 (CharField): Подтверждение пароля (ввод при регистрации).

    Атрибуты:
        Meta:
            model (Model): Модель, связанная с формой, в данном случае `User`.
            fields (tuple): Поля формы.
    """

    class Meta:
        model = User
        fields = (
            "email", "first_name", "last_name", "phone", "city", "country", "avatar", "password1", "password2")


class UserProfileForm(UserChangeForm, StyleFormMixin):
    """
    Форма для обновления профиля пользователя.

    Наследует от `UserChangeForm` и `StyleFormMixin`. Позволяет пользователю обновить свою информацию.

    Поля:
        first_name (CharField): Имя пользователя.
        last_name (CharField): Фамилия пользователя.
        email (EmailField): Адрес электронной почты пользователя.
        phone (CharField): Телефонный номер пользователя.
        city (CharField): Город проживания пользователя.
        country (CharField): Страна проживания пользователя.
        avatar (ImageField): Аватар пользователя.
        birth_date (DateField): Дата рождения пользователя.

    Атрибуты:
        Meta:
            model (Model): Модель, связанная с формой, в данном случае `User`.
            fields (tuple): Поля формы.
            widgets (dict): Виджеты для полей формы, в данном случае для `birth_date` используется виджет `DateInput`.
    """

    class Meta:
        model = User
        fields = ("first_name", "last_name", "email", "phone", "city", "country", "avatar")
        widgets = {
            'birth_date': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password'].widget = forms.HiddenInput()


class CustomAuthenticationForm(AuthenticationForm):
    """
    Кастомизированная форма для аутентификации пользователя.

    Наследует от `AuthenticationForm` и добавляет проверку на подтверждение электронной почты.
    """

    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    def confirm_login_allowed(self, user):
        """
        Проверяет, что пользователь подтвердил свою электронную почту.

        Аргументы:
            user (User): Пользователь, который пытается войти.

        Исключение:
            forms.ValidationError: Выбрасывается, если почта пользователя не подтверждена.
        """
        if not user.is_verified:
            raise forms.ValidationError(
                "Вы должны подтвердить вашу электронную почту, чтобы войти.",
                code='inactive',
            )
