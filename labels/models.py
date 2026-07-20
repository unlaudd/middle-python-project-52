"""
Label model for the labels application.
"""
from django.db import models
from django.utils.translation import gettext_lazy as _


class Label(models.Model):
    """
    Model representing a task label (e.g., 'bug', 'feature').
    Labels are used to categorize and group tasks.
    """
    name = models.CharField(_('Name'), max_length=50, unique=True)
    created_at = models.DateTimeField(_('Created at'), auto_now_add=True)

    def __str__(self):
        return self.name
