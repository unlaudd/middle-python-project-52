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
            'name': _('Имя'),
            'description': _('Описание'),
            'status': _('Статус'),
            'assignee': _('Исполнитель'),
            'labels': _('Метки'),
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
        self.fields['assignee'].label_from_instance = lambda obj: f"{obj.first_name} {obj.last_name}".strip() or obj.username