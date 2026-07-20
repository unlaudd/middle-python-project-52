"""
Admin configuration for the tasks application.
"""
from django.contrib import admin

from .models import Task


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    """
    Admin configuration for the Task model.
    """
    list_display = ('id', 'name', 'status', 'author', 'assignee', 'created_at')
    list_filter = ('status', 'author', 'assignee', 'created_at')
    search_fields = ('name', 'description')
    ordering = ('-created_at',)
