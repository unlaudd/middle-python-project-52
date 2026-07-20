"""
Forms for the tasks application.
"""
from django import forms
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _

from statuses.models import Status

from .models import Task


class TaskForm(forms.ModelForm):
    """
    Form for creating and updating tasks.
    """

    class Meta:
        model = Task
        fields = ['name', 'description', 'status', 'assignee', 'labels']
        labels = {
            'name': _('Name'),
            'description': _('Description'),
            'status': _('Status'),
            'assignee': _('Assignee'),
            'labels': _('Labels'),
        }
        widgets = {
            'labels': forms.SelectMultiple(attrs={'class': 'form-select', 'size': '5'}),
        }

    def __init__(self, *args, **kwargs):
        """
        Initialize the form and set querysets for related fields.
        """
        super().__init__(*args, **kwargs)
        self.fields['status'].queryset = Status.objects.all()
        self.fields['assignee'].queryset = User.objects.all()
