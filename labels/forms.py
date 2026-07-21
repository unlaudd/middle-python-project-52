# labels/forms.py
"""
Forms for the labels application.

This module provides form classes for creating and updating
task labels used throughout the task management system.
"""
from django import forms
from django.utils.translation import gettext_lazy as _

from .models import Label


class LabelForm(forms.ModelForm):
    """
    Form for creating and updating task labels.

    This ModelForm is bound to the Label model and exposes only the
    'name' field for editing. It is used by both the label creation
    and update views, providing a consistent interface for label
    management across the application.

    Fields:
        name (CharField): The display name of the label. Must be unique
            and is limited to 50 characters.

    Usage:
        Typically instantiated in CreateView and UpdateView for the
        Label model. The form handles validation of the label name
        automatically through the underlying model constraints.
    """
    name = forms.CharField(label=_('Имя'), max_length=50)

    class Meta:
        model = Label
        fields = ['name']
