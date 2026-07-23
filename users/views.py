"""
Views for user management, authentication, and profile operations.

This module provides class-based views for handling user registration,
login, logout, profile updates, and user deletion.
"""
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView, LogoutView, redirect_to_login
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from .forms import LoginForm, UserRegistrationForm, UserUpdateForm


class UserListView(ListView):
    """
    View for displaying a list of all users.

    Permissions:
        Public access - no authentication required.

    Context:
        users (QuerySet): All User objects in the database.

    Returns:
        HttpResponse: Renders 'users/list.html' with the user list.
    """
    model = User
    template_name = 'users/list.html'
    context_object_name = 'users'


class UserCreateView(SuccessMessageMixin, CreateView):
    """
    View for registering a new user.

    Handles user registration with success message display.
    After successful registration, redirects to the login page.

    Permissions:
        Public access - no authentication required.

    Context:
        form (UserRegistrationForm): Registration form instance.

    Returns:
        HttpResponse: Renders 'users/create.html' on GET request.
        HttpResponseRedirect: Redirects to login page on successful POST.
    """
    model = User
    form_class = UserRegistrationForm
    template_name = 'users/create.html'
    success_url = reverse_lazy('login')
    success_message = _('Пользователь успешно зарегистрирован')


class CustomLoginView(SuccessMessageMixin, LoginView):
    """
    View for user authentication.

    Handles user login with success message display.
    After successful login, redirects to the home page.

    Permissions:
        Public access - no authentication required.

    Context:
        form (LoginForm): Login form instance.

    Returns:
        HttpResponse: Renders 'users/login.html' on GET request.
        HttpResponseRedirect: Redirects to home page on successful POST.
    """
    form_class = LoginForm
    template_name = 'users/login.html'
    success_message = _('Вы залогинены')

    def get_success_url(self):
        """
        Get the URL to redirect to after successful login.

        Returns:
            str: URL for the home page.
        """
        return reverse_lazy('home')


class CustomLogoutView(LogoutView):
    """
    View for user logout.

    Handles user logout and displays a logout message.
    After logout, redirects to the home page.

    Permissions:
        Requires authentication.

    Returns:
        HttpResponseRedirect: Redirects to home page after logout.
    """
    next_page = reverse_lazy('home')

    def dispatch(self, request, *args, **kwargs):
        """
        Handle the logout request and add a flash message.

        Args:
            request (HttpRequest): The HTTP request object.

        Returns:
            HttpResponseRedirect: Redirect response after logout.
        """
        messages.info(request, _('Вы разлогинены'))
        return super().dispatch(request, *args, **kwargs)


class UserUpdateView(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, UpdateView):  # noqa: E501
    """
    View for updating a user's profile.

    Allows users to update their own profile information including
    name, username, and optionally password.

    Permissions:
        Requires authentication. Users can only update their own profile.

    Context:
        form (UserUpdateForm): Update form instance.
        object (User): The user being updated.

    Returns:
        HttpResponse: Renders 'users/update.html' on GET request.
        HttpResponseRedirect: Redirects to users list on successful POST.
    """
    model = User
    form_class = UserUpdateForm
    template_name = 'users/update.html'
    success_url = reverse_lazy('users_list')
    success_message = _('Пользователь успешно изменен')

    def test_func(self):
        """
        Check if the current user is the owner of the profile.

        Returns:
            bool: True if user can update this profile, False otherwise.
        """
        return self.request.user == self.get_object()

    def handle_no_permission(self):
        """
        Handle unauthorized access attempts.

        Redirects unauthenticated users to login page.
        Shows error message for authenticated users trying to update
        another user's profile.

        Returns:
            HttpResponseRedirect: Redirect response to appropriate page.
        """
        if not self.request.user.is_authenticated:
            return redirect_to_login(self.request.get_full_path())
        messages.error(self.request, _('У вас нет прав для изменения этого пользователя.'))  # noqa: E501
        return redirect('users_list')


class UserDeleteView(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, DeleteView):  # noqa: E501
    """
    View for deleting a user account.

    Allows users to delete their own account. Prevents deletion
    if the user is referenced by tasks (author or assignee).

    Permissions:
        Requires authentication. Users can only delete their own account.

    Context:
        object (User): The user being deleted.

    Returns:
        HttpResponse: Renders 'users/delete.html' on GET request.
        HttpResponseRedirect: Redirects to users list on successful POST.
    """
    model = User
    template_name = 'users/delete.html'
    success_url = reverse_lazy('users_list')
    success_message = _('Пользователь успешно удален')

    def test_func(self):
        """
        Check if the current user is the owner of the account.

        Returns:
            bool: True if user can delete this account, False otherwise.
        """
        return self.request.user == self.get_object()

    def handle_no_permission(self):
        """
        Handle unauthorized access attempts.

        Redirects unauthenticated users to login page.
        Shows error message for authenticated users trying to delete
        another user's account.

        Returns:
            HttpResponseRedirect: Redirect response to appropriate page.
        """
        if not self.request.user.is_authenticated:
            return redirect_to_login(self.request.get_full_path())
        messages.error(self.request, _('У вас нет прав для изменения этого пользователя.'))  # noqa: E501
        return redirect('users_list')

    def post(self, request, *args, **kwargs):
        """
        Handle user deletion with protection against linked tasks.

        Checks whether the user is associated with any tasks before
        attempting deletion. If tasks exist, displays an error message
        and redirects without deleting. Otherwise, proceeds with the
        standard deletion flow.

        Args:
            request (HttpRequest): The HTTP POST request object.
            *args: Additional positional arguments.
            **kwargs: URL keyword arguments (includes 'pk' of the user).

        Returns:
            HttpResponseRedirect: Redirects to users list with either
                a success or error flash message.
        """
        self.object = self.get_object()
        if self.object.authored_tasks.exists() or self.object.assigned_tasks.exists():  # noqa: E501
            messages.error(self.request, _('Невозможно удалить пользователя, связанного с задачами'))  # noqa: E501
            return redirect(self.success_url)
        return super().post(request, *args, **kwargs)
