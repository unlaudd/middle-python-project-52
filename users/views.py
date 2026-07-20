"""
Views for user management, authentication, and profile operations.
"""
import sys
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView, LogoutView, redirect_to_login
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import ProtectedError
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from .forms import LoginForm, UserRegistrationForm, UserUpdateForm


class UserListView(ListView):
    model = User
    template_name = 'users/list.html'
    context_object_name = 'users'


class UserCreateView(SuccessMessageMixin, CreateView):
    model = User
    form_class = UserRegistrationForm
    template_name = 'users/create.html'
    success_url = reverse_lazy('login')
    success_message = _('Пользователь успешно зарегистрирован')

    def form_invalid(self, form):
        # Принудительный вывод ошибок валидации в лог Docker (stderr с flush)
        print("=== FORM VALIDATION ERRORS ===", flush=True, file=sys.stderr)
        print(form.errors, flush=True, file=sys.stderr)
        print("==============================", flush=True, file=sys.stderr)
        return super().form_invalid(form)


class CustomLoginView(SuccessMessageMixin, LoginView):
    form_class = LoginForm
    template_name = 'users/login.html'
    success_message = _('Вы вошли в систему')

    def get_success_url(self):
        return reverse_lazy('home')


class CustomLogoutView(LogoutView):
    next_page = reverse_lazy('home')

    def dispatch(self, request, *args, **kwargs):
        messages.info(request, _('Вы вышли из системы'))
        return super().dispatch(request, *args, **kwargs)


class UserUpdateView(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, UpdateView):
    model = User
    form_class = UserUpdateForm
    template_name = 'users/update.html'
    success_url = reverse_lazy('users_list')
    success_message = _('Пользователь успешно обновлен')

    def test_func(self):
        return self.request.user == self.get_object()

    def handle_no_permission(self):
        if not self.request.user.is_authenticated:
            return redirect_to_login(self.request.get_full_path())
        messages.error(self.request, _('У вас нет прав для изменения этого пользователя.'))
        return redirect('users_list')


class UserDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = User
    template_name = 'users/delete.html'
    success_url = reverse_lazy('users_list')

    def test_func(self):
        return self.request.user == self.get_object()

    def handle_no_permission(self):
        if not self.request.user.is_authenticated:
            return redirect_to_login(self.request.get_full_path())
        messages.error(self.request, _('У вас нет прав для изменения этого пользователя.'))
        return redirect('users_list')

    def delete(self, request, *args, **kwargs):
        try:
            response = super().delete(request, *args, **kwargs)
            messages.success(self.request, _('Пользователь успешно удален'))
            return response
        except ProtectedError:
            messages.error(self.request, _('Невозможно удалить пользователя, связанного с задачами'))
            return redirect(self.success_url)
