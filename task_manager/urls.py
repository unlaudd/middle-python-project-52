"""
URL configuration for the task_manager project.

This module defines the root URL patterns for the application, routing requests
to the appropriate views and including URL configurations from individual apps.

URL Patterns:
    - 'admin/': Django administration interface.
    - '': Home page (HomeView).
    - 'login/': User authentication (CustomLoginView).
    - 'logout/': User logout (CustomLogoutView).
    - 'users/': User management operations (included from users.urls).
    - 'statuses/': Status management operations (included from statuses.urls).
    - 'tasks/': Task management operations (included from tasks.urls).
    - 'labels/': Label management operations (included from labels.urls).
"""
from django.contrib import admin
from django.urls import include, path

from .views import HomeView
from users.views import CustomLoginView, CustomLogoutView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', HomeView.as_view(), name='home'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    path('users/', include('users.urls')),
    path('statuses/', include('statuses.urls')),
    path('tasks/', include('tasks.urls')),
    path('labels/', include('labels.urls')),
]
