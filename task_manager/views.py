"""
Views for the main task_manager application.
"""
from django.views.generic import TemplateView


class HomeView(TemplateView):
    """
    View for the application home page.
    """
    template_name = 'home.html'