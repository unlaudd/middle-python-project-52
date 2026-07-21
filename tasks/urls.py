"""
URL configuration for the tasks application.

This module defines URL patterns for managing tasks, including listing,
creating, viewing details, updating, and deleting tasks.

URL Patterns:
    - '' (GET): Display paginated list of all tasks with filtering options
    - 'create/' (GET, POST): Create a new task
    - '<int:pk>/' (GET): View detailed information about a specific task
    - '<int:pk>/update/' (GET, POST): Update an existing task
    - '<int:pk>/delete/' (GET, POST): Delete a task

Permissions:
    All views require user authentication (LoginRequiredMixin).
    Task deletion is restricted to the task author only.

Notes:
    The task list view supports filtering by status, assignee, labels,
    and "only my tasks" option. Filters are applied via GET parameters.
"""
from django.urls import path

from .views import (
    TaskCreateView,
    TaskDeleteView,
    TaskDetailView,
    TaskListView,
    TaskUpdateView,
)

urlpatterns = [
    # List all tasks with filtering capabilities
    path('', TaskListView.as_view(), name='tasks_list'),
    
    # Create a new task
    path('create/', TaskCreateView.as_view(), name='tasks_create'),
    
    # View detailed information about a specific task
    path('<int:pk>/', TaskDetailView.as_view(), name='tasks_detail'),
    
    # Update an existing task
    path('<int:pk>/update/', TaskUpdateView.as_view(), name='tasks_update'),
    
    # Delete a task (author only)
    path('<int:pk>/delete/', TaskDeleteView.as_view(), name='tasks_delete'),
]
