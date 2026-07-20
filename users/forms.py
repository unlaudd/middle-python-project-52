"""
Forms for user registration, authentication, and profile updates.
"""
from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _


class UserRegistrationForm(UserCreationForm):
    """
    Form for registering a new user with first name, last name, and username.
    """
    first_name = forms.CharField(
        label=_('Имя'),
        max_length=30,
        required=True
    )
    last_name = forms.CharField(
        label=_('Фамилия'),
        max_length=30,
        required=True
    )
    username = forms.CharField(
        label=_('Имя пользователя'),
        max_length=150,
        required=True
    )
    password1 = forms.CharField(
        label=_('Пароль'),
        widget=forms.PasswordInput,
        required=True
    )
    password2 = forms.CharField(
        label=_('Подтверждение пароля'),
        widget=forms.PasswordInput,
        required=True,
        help_text=_('Введите тот же пароль, что и ранее, для проверки.')
    )

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'password1', 'password2')

    def save(self, commit=True):
        """
        Save the user with first name and last name from the form data.
        """
        user = super().save(commit=False)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        if commit:
            user.save()
        return user


class UserUpdateForm(forms.ModelForm):
    """
    Form for updating user profile information.
    """
    first_name = forms.CharField(
        label=_('Имя'),
        max_length=30,
        required=True
    )
    last_name = forms.CharField(
        label=_('Фамилия'),
        max_length=30,
        required=True
    )
    username = forms.CharField(
        label=_('Имя пользователя'),
        max_length=150,
        required=True
    )

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username')


class LoginForm(AuthenticationForm):
    """
    Form for user authentication.
    """
    username = forms.CharField(
        label=_('Имя пользователя'),
        max_length=150,
        required=True
    )
    password = forms.CharField(
        label=_('Пароль'),
        widget=forms.PasswordInput,
        required=True
    )
