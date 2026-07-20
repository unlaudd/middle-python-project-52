"""
URL configuration for the task_manager project.
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
