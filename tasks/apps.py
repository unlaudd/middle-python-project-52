"""
Tasks application configuration.

This module defines the Django application configuration for the tasks app,
which is the core component of the task management system. It handles
registration of the application with Django, including model discovery,
admin integration, and internationalization settings.

The tasks app manages the full lifecycle of tasks, including creation,
assignment, status tracking, labeling, and deletion, with support for
filtering and access control based on task authorship.
"""
from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class TasksConfig(AppConfig):
    """
    Configuration class for the tasks application.

    Registers the tasks app with Django's application registry and
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
        'tasks' is listed in the INSTALLED_APPS setting.
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'tasks'
    verbose_name = _('Tasks')
