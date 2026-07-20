"""
Tasks application configuration.
"""
from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class TasksConfig(AppConfig):
    """
    Configuration class for the tasks application.
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'tasks'
    verbose_name = _('Tasks')
