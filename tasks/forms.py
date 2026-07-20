from django import forms
from django.utils.translation import gettext_lazy as _
from .models import Task, Label
from statuses.models import Status
from django.contrib.auth.models import User

class TaskForm(forms.ModelForm):
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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['status'].queryset = Status.objects.all()
        self.fields['assignee'].queryset = User.objects.all()
        self.fields['labels'].queryset = Label.objects.all()
        self.fields['assignee'].required = False
        self.fields['labels'].required = False
