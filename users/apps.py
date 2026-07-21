"""
Users application configuration.

This module defines the Django application configuration for the users app,
which handles all user-related operations within the task management system,
including user registration, authentication, profile management, and
account deletion.

The users app leverages Django's built-in User model from
``django.contrib.auth`` and extends it with custom forms and views to
provide the application-specific registration and profile update workflows.
It is registered with Django's application registry to enable model
discovery, admin integration, and internationalization of the application
label.
"""
from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class UsersConfig(AppConfig):
    """
    Configuration class for the users application.

    Registers the users app with Django's application registry and
    configures application-level settings such as the default primary
    key field type and the human-readable application name.

    Attributes:
        default_auto_field (str): The type of auto-incrementing primary key
            to use for models in this app that do not explicitly define one.
            Defaults to Django's BigAutoField for compatibility with large
            datasets.
        name (str): The Python import path of the application, used by
            Django to locate and load the app.
        verbose_name (str): A human-readable, translatable name for the
            application, displayed in the Django admin interface and other
            administrative contexts.

    Usage:
        This configuration is automatically discovered by Django when
        'users' is listed in the INSTALLED_APPS setting.
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'users'
    verbose_name = _('Users')
