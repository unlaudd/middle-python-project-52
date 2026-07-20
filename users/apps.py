"""
Users application configuration.
"""
from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class UsersConfig(AppConfig):
    """
    Configuration class for the users application.
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'users'
    verbose_name = _('Users')
