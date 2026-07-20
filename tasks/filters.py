"""
Filters for the tasks application.
"""
import django_filters
from django import forms
from django.utils.translation import gettext_lazy as _

from .models import Task


class TaskFilter(django_filters.FilterSet):
    """
    FilterSet for filtering tasks by status, assignee, labels, and author.
    """
    only_my_tasks = django_filters.BooleanFilter(
        label=_('Only my tasks'),
        method='filter_only_my_tasks',
        widget=forms.CheckboxInput()
    )

    class Meta:
        model = Task
        fields = ['status', 'assignee', 'labels', 'only_my_tasks']
        labels = {
            'status': _('Status'),
            'assignee': _('Assignee'),
            'labels': _('Label'),
        }

    def filter_only_my_tasks(self, queryset, name, value):
        """
        Filter tasks to show only those authored by the current user.
        """
        if value and self.request.user.is_authenticated:
            return queryset.filter(author=self.request.user)
        return queryset
