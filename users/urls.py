"""
URL configuration for the users application.
"""
from django.urls import path

from .views import (
    UserCreateView,
    UserDeleteView,
    UserListView,
    UserUpdateView,
)

urlpatterns = [
    path('', UserListView.as_view(), name='users_list'),
    path('create/', UserCreateView.as_view(), name='users_create'),
    path('<int:pk>/update/', UserUpdateView.as_view(), name='users_update'),
    path('<int:pk>/delete/', UserDeleteView.as_view(), name='users_delete'),
]
