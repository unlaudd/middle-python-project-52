"""
Views for task management operations.

This module provides class-based views for performing CRUD operations on tasks,
including listing with filtering, detailed viewing, creation, updating, and
deletion. All views require user authentication.
"""
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, UpdateView
from django_filters.views import FilterView

from .filters import TaskFilter
from .forms import TaskForm
from .models import Task


class TaskListView(LoginRequiredMixin, FilterView):
    """
    Display a filtered list of tasks.

    This view combines Django's FilterView with LoginRequiredMixin to provide
    authenticated users with a filterable task list. Tasks can be filtered by
    status, assignee, labels, and ownership using the TaskFilter filterset.

    Permissions:
        Requires user authentication (LoginRequiredMixin).

    Context:
        tasks (QuerySet[Task]): Filtered task objects based on GET parameters.
        filter (TaskFilter): Filter instance for rendering the filter form.

    Returns:
        HttpResponse: Renders 'tasks/list.html' with the filtered task list
            and filter form.
    """
    model = Task
    template_name = 'tasks/list.html'
    context_object_name = 'tasks'
    filterset_class = TaskFilter


class TaskDetailView(LoginRequiredMixin, DetailView):
    """
    Display detailed information about a specific task.

    This view shows all attributes of a single task including name, description,
    status, author, assignee, labels, and creation timestamp.

    Permissions:
        Requires user authentication (LoginRequiredMixin).

    Context:
        task (Task): The task object with all its attributes.

    Returns:
        HttpResponse: Renders 'tasks/detail.html' with the task details.
    """
    model = Task
    template_name = 'tasks/detail.html'
    context_object_name = 'task'


class TaskCreateView(LoginRequiredMixin, CreateView):
    """
    Create a new task.

    This view handles task creation through a form. The currently authenticated
    user is automatically set as the task author upon successful form submission.
    A success message is displayed after creation.

    Permissions:
        Requires user authentication (LoginRequiredMixin).

    Context:
        form (TaskForm): The task creation form instance.

    Returns:
        HttpResponse: Renders 'tasks/create.html' on GET request.
        HttpResponseRedirect: Redirects to tasks list on successful POST
            with a success flash message.
    """
    model = Task
    form_class = TaskForm
    template_name = 'tasks/create.html'
    success_url = reverse_lazy('tasks_list')

    def form_valid(self, form):
        """
        Set the current user as the task author and save the task.

        This method is called when the form validation passes. It assigns
        the currently authenticated user as the task author before saving
        the task to the database.

        Args:
            form (TaskForm): The validated form instance.

        Returns:
            HttpResponseRedirect: Redirect response to the tasks list page
                after successful task creation.
        """
        form.instance.author = self.request.user
        messages.success(self.request, 'Задача успешно создана')
        return super().form_valid(form)


class TaskUpdateView(LoginRequiredMixin, UpdateView):
    """
    Update an existing task.

    This view handles task modification through a form. All task attributes
    can be updated including name, description, status, assignee, and labels.
    A success message is displayed after successful update.

    Permissions:
        Requires user authentication (LoginRequiredMixin).

    Context:
        form (TaskForm): The task update form instance pre-filled with
            current task data.
        task (Task): The task object being updated.

    Returns:
        HttpResponse: Renders 'tasks/update.html' on GET request.
        HttpResponseRedirect: Redirects to tasks list on successful POST
            with a success flash message.
    """
    model = Task
    form_class = TaskForm
    template_name = 'tasks/update.html'
    success_url = reverse_lazy('tasks_list')

    def form_valid(self, form):
        """
        Save the updated task and display a success message.

        This method is called when the form validation passes. It saves
        the updated task data to the database and adds a success message
        to the request.

        Args:
            form (TaskForm): The validated form instance with updated data.

        Returns:
            HttpResponseRedirect: Redirect response to the tasks list page
                after successful task update.
        """
        messages.success(self.request, 'Задача успешно изменена')
        return super().form_valid(form)


class TaskDeleteView(LoginRequiredMixin, DeleteView):
    """
    Delete an existing task.

    This view handles task deletion with authorization checks. Only the task
    author is permitted to delete the task. If a non-author attempts deletion,
    an error message is displayed and the user is redirected to the tasks list.
    A success message is displayed after successful deletion.

    Permissions:
        Requires user authentication (LoginRequiredMixin).
        Only the task author can delete the task.

    Context:
        task (Task): The task object being deleted.

    Returns:
        HttpResponse: Renders 'tasks/delete.html' on GET request (if authorized).
        HttpResponseRedirect: Redirects to tasks list on successful POST
            with a success flash message, or with an error message if
            the user is not the task author.
    """
    model = Task
    template_name = 'tasks/delete.html'
    success_url = reverse_lazy('tasks_list')

    def dispatch(self, request, *args, **kwargs):
        """
        Check if the current user is the task author before processing the request.

        This method intercepts the request before it reaches the view handler.
        It verifies that the authenticated user is the author of the task.
        If not, it displays an error message and redirects to the tasks list.

        Args:
            request (HttpRequest): The HTTP request object.
            *args: Additional positional arguments from the URL pattern.
            **kwargs: Additional keyword arguments from the URL pattern
                (includes 'pk' identifying the task to delete).

        Returns:
            HttpResponse: The response from the parent dispatch method if
                the user is authorized, or a redirect response with an error
                message if the user is not the task author.
        """
        self.object = self.get_object()
        if self.object.author != request.user:
            messages.error(request, 'Задачу может удалить только ее автор')
            return redirect('tasks_list')
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        """
        Delete the task and display a success message.

        This method handles the POST request for task deletion. It adds
        a success message to the request before delegating to the parent
        class's post method to perform the actual deletion.

        Args:
            request (HttpRequest): The HTTP POST request object.
            *args: Additional positional arguments from the URL pattern.
            **kwargs: Additional keyword arguments from the URL pattern.

        Returns:
            HttpResponseRedirect: Redirect response to the tasks list page
                after successful task deletion.
        """
        messages.success(request, 'Задача успешно удалена')
        return super().post(request, *args, **kwargs)
