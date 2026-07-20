"""
URL configuration for the labels application.
"""
from django.urls import path

from .views import (
    LabelCreateView,
    LabelDeleteView,
    LabelListView,
    LabelUpdateView,
)

urlpatterns = [
    path('', LabelListView.as_view(), name='labels_list'),
    path('create/', LabelCreateView.as_view(), name='labels_create'),
    path('<int:pk>/update/', LabelUpdateView.as_view(), name='labels_update'),
    path('<int:pk>/delete/', LabelDeleteView.as_view(), name='labels_delete'),
]
