"""
Forms for the statuses application.

This module provides form classes for creating and updating task statuses
within the task management system. Statuses represent the current state
of a task (e.g., 'New', 'In Progress', 'Completed') and are used to
track the workflow of tasks throughout their lifecycle.

The forms defined here are used by class-based views in the statuses
application to handle user input, validation, and persistence of status
records.
"""
from django import forms
from django.utils.translation import gettext_lazy as _

from .models import Status


class StatusForm(forms.ModelForm):
    """
    Form for creating and updating task statuses.

    This ModelForm is bound to the Status model and exposes the 'name'
    field for editing. It is used by both the StatusCreateView and
    StatusUpdateView to handle user input for status records.

    Fields:
        name (CharField): The display name of the status. Limited to
            100 characters. Uniqueness is enforced at the model level.

    Usage:
        Typically instantiated in CreateView and UpdateView for the
        Status model. The form handles validation of the status name
        automatically through the underlying model constraints.

    Note:
        Statuses cannot be deleted if they are associated with any tasks
        (enforced at the model level with on_delete=PROTECT). This form
        does not handle deletion logic directly.
    """
    name = forms.CharField(label=_('Имя'), max_length=100)

    class Meta:
        model = Status
        fields = ['name']
