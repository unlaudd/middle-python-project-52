"""
Task and Label models for the tasks application.
"""
from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _


class Label(models.Model):
    """
    Model representing a task label.
    Labels are used to categorize tasks (e.g., 'bug', 'feature').
    """
    name = models.CharField(_('Name'), max_length=50, unique=True)

    def __str__(self):
        return self.name


class Task(models.Model):
    """
    Model representing a task in the task management system.
    Tasks have a name, description, status, author, assignee, and labels.
    """
    name = models.CharField(_('Name'), max_length=100, unique=True)
    description = models.TextField(_('Description'), blank=True)
    status = models.ForeignKey(
        'statuses.Status', 
        on_delete=models.PROTECT, 
        verbose_name=_('Status')
    )
    author = models.ForeignKey(
        User, 
        on_delete=models.PROTECT, 
        related_name='authored_tasks', 
        verbose_name=_('Author')
    )
    assignee = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='assigned_tasks', 
        verbose_name=_('Assignee')
    )
    labels = models.ManyToManyField(
        'labels.Label', 
        blank=True, 
        verbose_name=_('Labels')
    )
    created_at = models.DateTimeField(_('Created at'), auto_now_add=True)

    def __str__(self):
        return self.name
