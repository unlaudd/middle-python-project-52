"""
Filters for the tasks application.

This module provides filtering capabilities for the task list view,
allowing authenticated users to narrow down tasks by various criteria
such as status, assignee, labels, and authorship. Filters are rendered
as a form above the task table and applied via GET parameters.

The TaskFilter class integrates with django-filter's FilterSet to
provide declarative filter definitions that are automatically rendered
in templates using django-bootstrap5.
"""
import django_filters
from django import forms
from django.utils.translation import gettext_lazy as _

from .models import Task


class TaskFilter(django_filters.FilterSet):
    """
    FilterSet for filtering tasks by status, assignee, labels, and author.

    Provides a set of filters that can be applied to the task queryset
    to display only tasks matching the specified criteria. All filters
    are optional and can be combined for more specific results.

    Attributes:
        only_my_tasks (BooleanFilter): A checkbox filter that restricts
            the queryset to tasks authored by the currently authenticated
            user. When unchecked or not provided, all tasks are shown.

    Meta:
        model: The Task model this filterset operates on.
        fields: List of model fields available for filtering, including
            status (ForeignKey), assignee (ForeignKey), labels (ManyToMany),
            and the custom only_my_tasks boolean filter.
        labels: Human-readable labels for each filter field, translated
            via gettext_lazy for internationalization support.

    Usage:
        Typically instantiated in TaskListView (a django-filter FilterView)
        and rendered in the task list template as a filter form. The
        filterset reads GET parameters from the request and applies
        the corresponding queryset filters automatically.

    Example:
        Filtering tasks by status and assignee via URL parameters:
        /tasks/?status=1&assignee=3&only_my_tasks=on
    """
    only_my_tasks = django_filters.BooleanFilter(
        label=_('Только свои задачи'),
        method='filter_only_my_tasks',
        widget=forms.CheckboxInput()
    )

    class Meta:
        model = Task
        fields = ['status', 'assignee', 'labels', 'only_my_tasks']
        labels = {
            'status': _('Статус'),
            'assignee': _('Исполнитель'),
            'labels': _('Метка'),
        }

    def filter_only_my_tasks(self, queryset, name, value):
        """
        Filter tasks to show only those authored by the current user.

        This custom filter method is invoked when the 'only_my_tasks'
        checkbox is toggled. It restricts the queryset to tasks where
        the author field matches the currently authenticated user.

        Args:
            queryset (QuerySet[Task]): The current task queryset to filter.
            name (str): The name of the filter field ('only_my_tasks').
            value (bool): The filter value. True if the checkbox is
                checked, False or None otherwise.

        Returns:
            QuerySet[Task]: The filtered queryset containing only tasks
                authored by the current user if value is True and the
                user is authenticated. Otherwise, returns the unmodified
                queryset.

        Note:
            This filter safely handles unauthenticated requests by
            returning the full queryset when no user is logged in,
            preventing AttributeError on anonymous users.
        """
        if value and self.request.user.is_authenticated:
            return queryset.filter(author=self.request.user)
        return queryset
