from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _


class UserRegistrationForm(UserCreationForm):
    first_name = forms.CharField(
        label=_('First name'),
        max_length=30,
        required=True
    )
    last_name = forms.CharField(
        label=_('Last name'),
        max_length=30,
        required=True
    )
    username = forms.CharField(
        label=_('Username'),
        max_length=150,
        required=True
    )
    password1 = forms.CharField(
        label=_('Password'),
        widget=forms.PasswordInput,
        required=True
    )
    password2 = forms.CharField(
        label=_('Password confirmation'),
        widget=forms.PasswordInput,
        required=True,
        help_text=_('Enter the same password as before, for verification.')
    )

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        if commit:
            user.save()
        return user


class UserUpdateForm(forms.ModelForm):
    first_name = forms.CharField(
        label=_('First name'),
        max_length=30,
        required=True
    )
    last_name = forms.CharField(
        label=_('Last name'),
        max_length=30,
        required=True
    )
    username = forms.CharField(
        label=_('Username'),
        max_length=150,
        required=True
    )

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username')


class LoginForm(AuthenticationForm):
    username = forms.CharField(
        label=_('Username'),
        max_length=150,
        required=True
    )
    password = forms.CharField(
        label=_('Password'),
        widget=forms.PasswordInput,
        required=True
    )
