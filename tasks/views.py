"""
Views for the tasks application.
"""
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import CreateView, DeleteView, DetailView, UpdateView
from django_filters.views import FilterView

from .filters import TaskFilter
from .forms import TaskForm
from .models import Task


class TaskListView(LoginRequiredMixin, FilterView):
    """
    View for displaying a filtered list of tasks.
    """
    model = Task
    template_name = 'tasks/list.html'
    context_object_name = 'tasks'
    filterset_class = TaskFilter


class TaskCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    """
    View for creating a new task.
    """
    model = Task
    form_class = TaskForm
    template_name = 'tasks/create.html'
    success_url = reverse_lazy('tasks_list')
    success_message = _('Задача успешно создана')

    def form_valid(self, form):
        """
        Set the current user as the task author before saving.
        """
        form.instance.author = self.request.user
        return super().form_valid(form)


class TaskUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    """
    View for updating an existing task.
    """
    model = Task
    form_class = TaskForm
    template_name = 'tasks/update.html'
    success_url = reverse_lazy('tasks_list')
    success_message = _('Задача успешно обновлена')


class TaskDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """
    View for deleting a task.
    """
    model = Task
    template_name = 'tasks/delete.html'
    success_url = reverse_lazy('tasks_list')

    def test_func(self):
        """
        Check if the current user is the author of the task.
        """
        return self.request.user == self.get_object().author

    def handle_no_permission(self):
        """
        Handle unauthorized access attempts with an error message.
        """
        messages.error(self.request, _('Задачу может удалить только ее автор'))
        return redirect('tasks_list')

    def delete(self, request, *args, **kwargs):
        """
        Delete the task and show a success message.
        """
        response = super().delete(request, *args, **kwargs)
        messages.success(request, _('Задача успешно удалена'))
        return response


class TaskDetailView(LoginRequiredMixin, DetailView):
    """
    View for displaying detailed information about a task.
    """
    model = Task
    template_name = 'tasks/detail.html'
    context_object_name = 'task'
