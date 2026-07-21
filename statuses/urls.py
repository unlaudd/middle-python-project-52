"""
URL configuration for the statuses application.

This module defines URL patterns for managing task statuses, including
listing, creating, updating, and deleting statuses.

URL Patterns:
    - '' (GET): Display list of all task statuses
    - 'create/' (GET, POST): Create a new task status
    - '<int:pk>/update/' (GET, POST): Update an existing task status
    - '<int:pk>/delete/' (GET, POST): Delete a task status

Permissions:
    All views require user authentication (LoginRequiredMixin).

Notes:
    Status deletion is protected - if a status is associated with any tasks,
    deletion will be prevented to maintain data integrity.
"""
from django.urls import path

from .views import (
    StatusCreateView,
    StatusDeleteView,
    StatusListView,
    StatusUpdateView,
)

urlpatterns = [
    path('', StatusListView.as_view(), name='statuses_list'),
    path('create/', StatusCreateView.as_view(), name='statuses_create'),
    path('<int:pk>/update/', StatusUpdateView.as_view(), name='statuses_update'),
    path('<int:pk>/delete/', StatusDeleteView.as_view(), name='statuses_delete'),
]
