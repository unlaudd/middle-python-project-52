"""
Admin configuration for the users application.

This module customizes the Django admin interface for the built-in User model.
It replaces the default UserAdmin with an extended version that provides
additional display fields, filters, and search capabilities tailored for
the task management system's administrative needs.

The default UserAdmin is unregistered first to avoid conflicts, then the
custom admin class is registered in its place.
"""
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

admin.site.unregister(User)


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    """
    Custom admin configuration for the User model with extended display fields.

    Extends Django's built-in UserAdmin to provide a more informative list view
    for managing users in the task management system. This configuration adds
    key user attributes to the list display, enables filtering by staff status
    and activity, and supports searching across common user fields.

    Attributes:
        list_display (tuple): Fields shown as columns in the admin list view.
            Includes user identification (id, username), personal information
            (first_name, last_name, email), administrative flags (is_staff),
            and registration date (date_joined).
        list_filter (tuple): Sidebar filters available in the admin list view.
            Allows filtering users by administrative status (is_staff,
            is_superuser), account state (is_active), and registration period
            (date_joined).
        search_fields (tuple): Fields searchable via the admin search bar.
            Enables text-based search across username, first_name, last_name,
            and email fields for quick user lookup.
        ordering (tuple): Default ordering for users in the admin list.
            Users are ordered by date_joined in descending order, showing
            the most recently registered users first.

    Usage:
        This admin class is automatically registered with the Django admin
        site when the users application is loaded. Administrators can access
        the user management interface at /admin/auth/user/.

    Note:
        The default UserAdmin is unregistered before this class is registered
        to prevent duplicate admin registrations for the User model.
    """
    list_display = ('id', 'username', 'first_name', 'last_name', 'email', 'is_staff', 'date_joined')  # noqa: E501
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'date_joined')
    search_fields = ('username', 'first_name', 'last_name', 'email')
    ordering = ('-date_joined',)
