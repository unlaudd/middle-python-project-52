"""
Views for label management operations.

This module provides class-based views for performing CRUD operations
on task labels, including listing, creating, updating, and deleting labels
with protection against deleting labels linked to existing tasks.
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

    Permissions:
        Requires user authentication (LoginRequiredMixin).

    Context:
        labels (QuerySet): All Label objects ordered by default model ordering.

    Returns:
        HttpResponse: Renders 'labels/list.html' with the list of labels.
    """
    model = Label
    template_name = 'labels/list.html'
    context_object_name = 'labels'


class LabelCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    """
    View for creating a new task label.

    Permissions:
        Requires user authentication (LoginRequiredMixin).

    Context:
        form (LabelForm): The label creation form instance.

    Returns:
        HttpResponse: Renders 'labels/create.html' on GET request.
        HttpResponseRedirect: Redirects to labels list on successful POST
            with a success flash message.
    """
    model = Label
    form_class = LabelForm
    template_name = 'labels/create.html'
    success_url = reverse_lazy('labels_list')
    success_message = _('Метка успешно создана')


class LabelUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    """
    View for updating an existing task label.

    Permissions:
        Requires user authentication (LoginRequiredMixin).

    Context:
        form (LabelForm): The label update form instance pre-filled with
            current label data.
        object (Label): The label instance being updated.

    Returns:
        HttpResponse: Renders 'labels/update.html' on GET request.
        HttpResponseRedirect: Redirects to labels list on successful POST
            with a success flash message.
    """
    model = Label
    form_class = LabelForm
    template_name = 'labels/update.html'
    success_url = reverse_lazy('labels_list')
    success_message = _('Метка успешно изменена')


class LabelDeleteView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    """
    View for deleting a task label.

    Prevents deletion if the label is associated with any tasks via
    the ManyToManyField relationship. In that case, an error message
    is displayed and the user is redirected back to the labels list.

    Permissions:
        Requires user authentication (LoginRequiredMixin).

    Context:
        object (Label): The label instance being deleted.

    Returns:
        HttpResponse: Renders 'labels/delete.html' on GET request.
        HttpResponseRedirect: Redirects to labels list on successful POST
            with a success flash message, or with an error message if
            the label is linked to tasks.
    """
    model = Label
    template_name = 'labels/delete.html'
    success_url = reverse_lazy('labels_list')
    success_message = _('Метка успешно удалена')

    def post(self, request, *args, **kwargs):
        """
        Handle label deletion with protection against linked tasks.

        Checks whether the label is associated with any tasks before
        attempting deletion. If tasks exist, displays an error message
        and redirects without deleting. Otherwise, proceeds with the
        standard deletion flow.

        Args:
            request (HttpRequest): The HTTP POST request object.
            *args: Additional positional arguments.
            **kwargs: URL keyword arguments (includes 'pk' of the label).

        Returns:
            HttpResponseRedirect: Redirects to labels list with either
                a success or error flash message.
        """
        self.object = self.get_object()
        if self.object.task_set.exists():
            messages.error(request, _('Невозможно удалить метку'))
            return redirect(self.success_url)

        return super().post(request, *args, **kwargs)
