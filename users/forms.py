"""
Forms for user registration, authentication, and profile updates.
"""
from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _


class UserRegistrationForm(UserCreationForm):
    first_name = forms.CharField(label=_('Имя'), max_length=150, required=True)
    last_name = forms.CharField(label=_('Фамилия'), max_length=150, required=True)

    class Meta(UserCreationForm.Meta):
        model = User
        # Наследуем стандартные поля UserCreationForm и добавляем свои
        fields = ('username', 'first_name', 'last_name', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = _('Имя пользователя')
        self.fields['password1'].label = _('Пароль')
        self.fields['password2'].label = _('Подтверждение пароля')
        self.fields['password2'].help_text = _('Введите тот же пароль, что и ранее, для проверки.')


class UserUpdateForm(forms.ModelForm):
    first_name = forms.CharField(label=_('Имя'), max_length=150, required=True)
    last_name = forms.CharField(label=_('Фамилия'), max_length=150, required=True)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = _('Имя пользователя')


class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = _('Имя пользователя')
        self.fields['password'].label = _('Пароль')
