"""
Views for status management operations.

This module provides class-based views for managing task statuses within
the task management system. Statuses represent workflow states (e.g.,
'New', 'In Progress', 'Done') that tasks can transition through.

The module enforces the following business rules:
    - Only authenticated users can manage statuses.
    - Statuses that are referenced by tasks cannot be deleted, preserving
      data integrity and task history.
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
    Display a paginated list of all task statuses.

    Permissions:
        Requires user authentication (LoginRequiredMixin).

    Context:
        statuses (QuerySet[Status]): All Status objects in the database,
            ordered by the model's default ordering.

    Returns:
        HttpResponse: Renders 'statuses/list.html' with the list of statuses.
    """
    model = Status
    template_name = 'statuses/list.html'
    context_object_name = 'statuses'


class StatusCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    """
    Create a new task status.

    Upon successful creation, displays a success flash message and redirects
    the user to the statuses list page.

    Permissions:
        Requires user authentication (LoginRequiredMixin).

    Context:
        form (StatusForm): An empty status creation form.

    Returns:
        HttpResponse: Renders 'statuses/create.html' on GET request.
        HttpResponseRedirect: Redirects to 'statuses_list' on successful POST
            with a success flash message.
    """
    model = Status
    form_class = StatusForm
    template_name = 'statuses/create.html'
    success_url = reverse_lazy('statuses_list')
    success_message = _('Статус успешно создан')


class StatusUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    """
    Update an existing task status.

    Upon successful update, displays a success flash message and redirects
    the user to the statuses list page.

    Permissions:
        Requires user authentication (LoginRequiredMixin).

    Context:
        form (StatusForm): A status update form pre-filled with the current
            status data.
        object (Status): The status instance being updated.

    Returns:
        HttpResponse: Renders 'statuses/update.html' on GET request.
        HttpResponseRedirect: Redirects to 'statuses_list' on successful POST
            with a success flash message.
    """
    model = Status
    form_class = StatusForm
    template_name = 'statuses/update.html'
    success_url = reverse_lazy('statuses_list')
    success_message = _('Статус успешно изменен')


class StatusDeleteView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    """
    Delete an existing task status.

    This view enforces a protection rule: if the status is referenced by
    one or more tasks (via the Task.status ForeignKey), the deletion is
    blocked and an error flash message is displayed instead. This preserves
    data integrity and prevents orphaned task references.

    If the status has no associated tasks, the deletion proceeds normally
    and a success flash message is displayed.

    Permissions:
        Requires user authentication (LoginRequiredMixin).

    Context:
        object (Status): The status instance being deleted.

    Returns:
        HttpResponse: Renders 'statuses/delete.html' on GET request.
        HttpResponseRedirect: Redirects to 'statuses_list' after POST,
            either with a success or an error flash message depending
            on whether the deletion was permitted.
    """
    model = Status
    template_name = 'statuses/delete.html'
    success_url = reverse_lazy('statuses_list')
    success_message = _('Статус успешно удален')

    def post(self, request, *args, **kwargs):
        """
        Handle the status deletion POST request with protection logic.

        Before delegating to the parent DeleteView, this method checks
        whether the status is referenced by any tasks. If so, it adds
        an error flash message and redirects to the statuses list without
        performing the deletion.

        Args:
            request (HttpRequest): The incoming HTTP POST request.
            *args: Additional positional arguments from the URL pattern.
            **kwargs: Additional keyword arguments from the URL pattern
                (includes 'pk' identifying the status to delete).

        Returns:
            HttpResponseRedirect: Redirects to 'statuses_list' with either
                an error message (if deletion is blocked) or delegates to
                the parent view for successful deletion.
        """
        self.object = self.get_object()
        if self.object.task_set.exists():
            messages.error(request, _('Невозможно удалить статус'))
            return redirect(self.success_url)
        
        return super().post(request, *args, **kwargs)
