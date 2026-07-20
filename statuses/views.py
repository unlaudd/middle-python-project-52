"""
Views for status management operations.
"""
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import ProtectedError
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from .forms import StatusForm
from .models import Status


class StatusListView(LoginRequiredMixin, ListView):
    """
    View for displaying a list of all task statuses.
    """
    model = Status
    template_name = 'statuses/list.html'
    context_object_name = 'statuses'


class StatusCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    """
    View for creating a new task status.
    """
    model = Status
    form_class = StatusForm
    template_name = 'statuses/create.html'
    success_url = reverse_lazy('statuses_list')
    success_message = _('Статус успешно создан')


class StatusUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    """
    View for updating an existing task status.
    """
    model = Status
    form_class = StatusForm
    template_name = 'statuses/update.html'
    success_url = reverse_lazy('statuses_list')
    success_message = _('Статус успешно обновлен')


class StatusDeleteView(LoginRequiredMixin, DeleteView):
    """
    View for deleting a task status.
    Prevents deletion if the status is linked to any tasks.
    """
    model = Status
    template_name = 'statuses/delete.html'
    success_url = reverse_lazy('statuses_list')

    def delete(self, request, *args, **kwargs):
        """
        Delete the status and show appropriate messages.
        """
        try:
            response = super().delete(request, *args, **kwargs)
            messages.success(request, _('Статус успешно удален'))
            return response
        except ProtectedError:
            messages.error(request, _('Невозможно удалить статус, связанный с задачами'))
            return redirect(self.success_url)