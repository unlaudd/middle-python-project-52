"""
Statuses application configuration.
"""
from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class StatusesConfig(AppConfig):
    """
    Configuration class for the statuses application.
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'statuses'
    verbose_name = _('Statuses')
