"""
Admin configuration for the statuses application.
"""
from django.contrib import admin

from .models import Status


@admin.register(Status)
class StatusAdmin(admin.ModelAdmin):
    """
    Admin configuration for the Status model.
    """
    list_display = ('id', 'name', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('name',)
    ordering = ('name',)
