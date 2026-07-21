"""
URL configuration for the labels application.

This module defines URL patterns for managing task labels, including
list, create, update, and delete operations.

URL Patterns:
    - '' (GET): Display list of all labels
    - 'create/' (GET, POST): Create a new label
    - '<int:pk>/update/' (GET, POST): Update an existing label
    - '<int:pk>/delete/' (GET, POST): Delete a label

Permissions:
    All views require user authentication (LoginRequiredMixin).
"""
from django.urls import path

from .views import (
    LabelCreateView,
    LabelDeleteView,
    LabelListView,
    LabelUpdateView,
)

urlpatterns = [
    # List all labels
    path('', LabelListView.as_view(), name='labels_list'),

    # Create a new label
    path('create/', LabelCreateView.as_view(), name='labels_create'),

    # Update an existing label (requires label ID)
    path('<int:pk>/update/', LabelUpdateView.as_view(), name='labels_update'),

    # Delete a label (requires label ID)
    path('<int:pk>/delete/', LabelDeleteView.as_view(), name='labels_delete'),
]
