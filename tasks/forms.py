"""
Forms for the tasks application.

This module provides form classes for creating and updating tasks within
the task management system. It includes a custom ModelChoiceField that
displays users by their full name (first name + last name) rather than
their username, improving the user experience when assigning tasks.

The TaskForm is bound to the Task model and exposes all editable fields
including name, description, status, executor (assignee), and labels.
It enforces uniqueness of task names and provides a multi-select widget
for label assignment.
"""
from django import forms
from django.contrib.auth.models import User

from .models import Task


class UserModelChoiceField(forms.ModelChoiceField):
    """
    A custom ModelChoiceField that displays User instances by their full name.

    Instead of showing the default string representation of a User (typically
    the username), this field renders each option as "FirstName LastName".
    If both first and last names are empty, it falls back to the username.

    This improves usability in task assignment dropdowns where users are
    more easily recognized by their real names than by their usernames.

    Example:
        A user with first_name="John", last_name="Doe", username="jdoe123"
        will appear in the dropdown as "John Doe" rather than "jdoe123".
    """

    def label_from_instance(self, user):
        """
        Return the display label for a given User instance.

        Constructs the label by concatenating the user's first and last names.
        If the resulting string is empty (both names are blank), falls back
        to the user's username to ensure every option has a non-empty label.

        Args:
            user (User): The User model instance to generate a label for.

        Returns:
            str: The display label for the user, formatted as
                "FirstName LastName" or the username as a fallback.
        """
        return f'{user.first_name} {user.last_name}'.strip() or user.username


class TaskForm(forms.ModelForm):
    """
    ModelForm for creating and updating tasks.

    Provides a form interface for all editable fields of the Task model,
    including a custom executor field that displays users by their full name.
    The labels field is rendered as a multi-select widget to allow assigning
    multiple labels to a single task.

    Attributes:
        executor (UserModelChoiceField): A custom choice field for selecting
            the task assignee. Displays users as "FirstName LastName" and
            is optional (not required).

    Meta:
        model (Task): The Task model this form is bound to.
        fields (list): The list of model fields exposed in the form.
        widgets (dict): Custom widget configuration for specific fields.
            The 'labels' field uses a SelectMultiple widget with 5 visible rows.
        labels (dict): Human-readable labels for each form field, used in
            the rendered HTML output.
        error_messages (dict): Custom validation error messages. Overrides
            the default uniqueness error for the 'name' field with a
            Russian-language message.

    Validation:
        - The 'name' field must be unique across all tasks. A duplicate name
          triggers the custom error message defined in Meta.error_messages.
        - The 'executor' field is optional; a task may exist without an assignee.
        - The 'labels' field accepts zero or more labels.

    Usage:
        Typically instantiated in TaskCreateView and TaskUpdateView. The form
        handles field rendering, validation, and persistence through the
        standard ModelForm workflow.
    """
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
