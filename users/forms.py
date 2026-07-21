"""
Forms for user registration, authentication, and profile updates.

This module provides form classes for handling all user-related operations
within the task management system. It includes forms for new user
registration, existing user profile updates, and user authentication
(login).

All forms use Django's built-in User model from django.contrib.auth and
apply Russian translations to field labels for a localized user experience.

Forms:
    - UserRegistrationForm: Handles new user registration with extended fields.
    - UserUpdateForm: Handles profile updates with optional password change.
    - LoginForm: Handles user authentication with localized labels.
"""
from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _


class UserRegistrationForm(UserCreationForm):
    """
    Form for registering a new user with first name, last name, and username.

    Extends Django's built-in UserCreationForm to include first_name and
    last_name fields, which are required for registration. This ensures that
    every user in the system has a complete profile from the moment of
    registration.

    Fields:
        first_name (CharField): User's first name. Required, max 150 characters.
        last_name (CharField): User's last name. Required, max 150 characters.
        username (CharField): Unique username. Inherited from UserCreationForm.
        password1 (CharField): Password. Inherited from UserCreationForm.
        password2 (CharField): Password confirmation. Inherited from UserCreationForm.

    Permissions:
        Public access - no authentication required. Any visitor can register.

    Usage:
        Used by UserCreateView to handle the registration flow. Upon successful
        submission, the user is created and redirected to the login page with
        a success flash message.

    Note:
        Field labels are overridden in __init__ to use Russian translations
        for consistency with the rest of the application's interface.
    """
    first_name = forms.CharField(label=_('Имя'), max_length=150, required=True)
    last_name = forms.CharField(label=_('Фамилия'), max_length=150, required=True)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'first_name', 'last_name')

    def __init__(self, *args, **kwargs):
        """
        Initialize the form and customize field labels.

        Overrides the default English labels from UserCreationForm with
        Russian translations to match the application's localization.

        Args:
            *args: Positional arguments passed to the parent constructor.
            **kwargs: Keyword arguments passed to the parent constructor.
        """
        super().__init__(*args, **kwargs)
        self.fields['username'].label = _('Имя пользователя')
        self.fields['password1'].label = _('Пароль')
        self.fields['password2'].label = _('Подтверждение пароля')


class UserUpdateForm(forms.ModelForm):
    """
    Form for updating user profile information.

    Allows authenticated users to update their profile details including
    first name, last name, username, and optionally change their password.
    The password fields are optional - if left empty, the existing password
    remains unchanged.

    Fields:
        first_name (CharField): User's first name. Required, max 150 characters.
        last_name (CharField): User's last name. Required, max 150 characters.
        username (CharField): Unique username. Required, max 150 characters.
        password1 (CharField): New password. Optional, rendered as PasswordInput.
        password2 (CharField): Password confirmation. Optional, rendered as PasswordInput.

    Permissions:
        Requires authentication. Users can only update their own profile.
        Enforced by UserPassesTestMixin in UserUpdateView.

    Usage:
        Used by UserUpdateView to handle profile update requests. The form
        is pre-populated with the current user's data and allows partial
        updates (e.g., only changing the name without touching the password).

    Note:
        The save() method is overridden to handle optional password changes.
        If password1 is provided, the password is updated via set_password()
        to ensure proper hashing. Otherwise, only profile fields are saved.
    """
    first_name = forms.CharField(label=_('Имя'), max_length=150, required=True)
    last_name = forms.CharField(label=_('Фамилия'), max_length=150, required=True)
    username = forms.CharField(label=_('Имя пользователя'), max_length=150, required=True)
    password1 = forms.CharField(
        label=_('Пароль'),
        widget=forms.PasswordInput,
        required=False
    )
    password2 = forms.CharField(
        label=_('Подтверждение пароля'),
        widget=forms.PasswordInput,
        required=False
    )

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'password1', 'password2')

    def save(self, commit=True):
        """
        Save the user with updated profile information and optional password change.

        If password1 is provided in the form data, the user's password is updated
        using set_password() to ensure proper hashing. Otherwise, only the profile
        fields (username, first_name, last_name) are saved.

        Args:
            commit (bool): Whether to save the user to the database immediately.
                Defaults to True. If False, the unsaved User instance is returned.

        Returns:
            User: The updated User instance, either saved to the database or
                pending save depending on the commit parameter.
        """
        user = super().save(commit=False)
        password = self.cleaned_data.get('password1')
        if password:
            user.set_password(password)
        if commit:
            user.save()
        return user


class LoginForm(AuthenticationForm):
    """
    Form for user authentication.

    Extends Django's built-in AuthenticationForm with Russian-translated
    field labels for a consistent user experience. Handles username and
    password validation, including checks for active user status and
    correct credentials.

    Fields:
        username (CharField): User's username for authentication.
        password (CharField): User's password for authentication.

    Permissions:
        Public access - no authentication required. Used by unauthenticated
        users to log into the system.

    Usage:
        Used by CustomLoginView to handle the login flow. Upon successful
        authentication, the user is redirected to the home page with a
        success flash message.

    Note:
        Inherits all validation logic from AuthenticationForm, including
        password verification and active user checks. Only the field
        labels are customized.
    """

    def __init__(self, *args, **kwargs):
        """
        Initialize the form and customize field labels.

        Overrides the default English labels from AuthenticationForm with
        Russian translations to match the application's localization.

        Args:
            *args: Positional arguments passed to the parent constructor.
            **kwargs: Keyword arguments passed to the parent constructor.
        """
        super().__init__(*args, **kwargs)
        self.fields['username'].label = _('Имя пользователя')
        self.fields['password'].label = _('Пароль')
