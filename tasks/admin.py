"""
Admin configuration for the tasks application.

This module registers the Task model with Django's admin interface,
providing a user-friendly interface for managing tasks in the backend.
It configures list display, filters, search functionality, and ordering
to facilitate efficient task administration.
"""
from django.contrib import admin

from .models import Task


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    """
    Admin configuration for the Task model.

    This class customizes the Django admin interface for Task objects,
    enabling administrators to efficiently view, search, filter, and
    manage tasks. It provides a comprehensive overview of task data
    with sortable columns and quick access to related objects.

    Attributes:
        list_display (tuple): Fields displayed in the admin list view.
            Includes task identification, status, authorship, assignment,
            and creation timestamp for quick reference.
        list_filter (tuple): Fields available for filtering in the admin
            sidebar. Allows filtering by status, author, assignee, and
            creation date to quickly locate specific tasks.
        search_fields (tuple): Fields searchable via the admin search bar.
            Enables text-based search across task names and descriptions.
        ordering (tuple): Default ordering for tasks in the admin list.
            Tasks are ordered by creation date in descending order,
            showing the most recently created tasks first.

    Usage:
        The Task model is automatically registered with the admin site
        through the @admin.register decorator. Administrators can access
        the task management interface at /admin/tasks/task/.
    """
    list_display = ('id', 'name', 'status', 'author', 'assignee', 'created_at')
    list_filter = ('status', 'author', 'assignee', 'created_at')
    search_fields = ('name', 'description')
    ordering = ('-created_at',)
