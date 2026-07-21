"""
URL configuration for the users application.

This module defines URL patterns for managing users within the task management
system, including listing, registration, profile updates, and account deletion.

URL Patterns:
    - '' (GET): Display list of all registered users
    - 'create/' (GET, POST): Register a new user account
    - '<int:pk>/update/' (GET, POST): Update an existing user's profile
    - '<int:pk>/delete/' (GET, POST): Delete a user account

Permissions:
    - Listing: Public access (no authentication required).
    - Creation: Public access (any visitor can register).
    - Update: Requires authentication. Users can only update their own profile.
    - Deletion: Requires authentication. Users can only delete their own account.
        Deletion is blocked if the user is referenced by any tasks (author or
        assignee) to preserve data integrity.

Notes:
    All user management views use class-based views (CBVs) for consistency
    and maintainability. Authentication and authorization are enforced through
    Django's LoginRequiredMixin and UserPassesTestMixin where applicable.
"""
from django.urls import path

from .views import (
    UserCreateView,
    UserDeleteView,
    UserListView,
    UserUpdateView,
)

urlpatterns = [
    # List all registered users
    path('', UserListView.as_view(), name='users_list'),

    # Register a new user account
    path('create/', UserCreateView.as_view(), name='users_create'),

    # Update an existing user's profile (self only)
    path('<int:pk>/update/', UserUpdateView.as_view(), name='users_update'),

    # Delete a user account (self only, blocked if referenced by tasks)
    path('<int:pk>/delete/', UserDeleteView.as_view(), name='users_delete'),
]
