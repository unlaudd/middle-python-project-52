"""
Status model for the statuses application.
"""
from django.db import models
from django.utils.translation import gettext_lazy as _


class Status(models.Model):
    """
    Model representing a task status (e.g., 'New', 'In Progress', 'Done').
    """
    name = models.CharField(_('Name'), max_length=100, unique=True)
    created_at = models.DateTimeField(_('Created at'), auto_now_add=True)

    def __str__(self):
        return self.name
