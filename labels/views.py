"""
Views for label management operations.
"""
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from .forms import LabelForm
from .models import Label


class LabelListView(LoginRequiredMixin, ListView):
    """
    View for displaying a list of all task labels.
    """
    model = Label
    template_name = 'labels/list.html'
    context_object_name = 'labels'


class LabelCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    """
    View for creating a new task label.
    """
    model = Label
    form_class = LabelForm
    template_name = 'labels/create.html'
    success_url = reverse_lazy('labels_list')
    success_message = _('Label successfully created')


class LabelUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    """
    View for updating an existing task label.
    """
    model = Label
    form_class = LabelForm
    template_name = 'labels/update.html'
    success_url = reverse_lazy('labels_list')
    success_message = _('Label successfully updated')


class LabelDeleteView(LoginRequiredMixin, DeleteView):
    """
    View for deleting a task label.
    Prevents deletion if the label is linked to any tasks.
    """
    model = Label
    template_name = 'labels/delete.html'
    success_url = reverse_lazy('labels_list')

    def post(self, request, *args, **kwargs):
        """
        Handle label deletion with protection against linked labels.
        """
        self.object = self.get_object()
        if self.object.task_set.exists():
            messages.error(request, _('Unable to delete label'))
            return redirect(self.success_url)
        return super().post(request, *args, **kwargs)
