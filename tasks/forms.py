from django import forms
from django.contrib.auth.models import User
from .models import Task


class UserModelChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, user):
        return f'{user.first_name} {user.last_name}'.strip() or user.username


class TaskForm(forms.ModelForm):
    executor = UserModelChoiceField(
        queryset=User.objects.all(),
        label='Исполнитель',
        required=False,
    )

    class Meta:
        model = Task
        fields = ['name', 'description', 'status', 'executor', 'labels']
        widgets = {
            'labels': forms.SelectMultiple(attrs={'class': 'form-select', 'size': '5'}),
        }
        labels = {
            'name': 'Имя',
            'description': 'Описание',
            'status': 'Статус',
            'executor': 'Исполнитель',
            'labels': 'Метки',
        }
        error_messages = {
            'name': {
                'unique': 'Задача с таким именем уже существует.'
            }
        }
