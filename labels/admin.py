"""
Admin configuration for the labels application.
"""
from django.contrib import admin

from .models import Label


@admin.register(Label)
class LabelAdmin(admin.ModelAdmin):
    """
    Admin configuration for the Label model.
    """
    list_display = ('id', 'name', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('name',)
    ordering = ('name',)
