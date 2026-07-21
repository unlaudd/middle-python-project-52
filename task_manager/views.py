"""
Views for the main task_manager application.

This module contains views for the core application functionality,
including the home page that serves as the entry point for all users.
"""
from django.views.generic import TemplateView


class HomeView(TemplateView):
    """
    View for the application home page.

    Renders the main landing page of the task management application.
    This view is accessible to all users regardless of authentication status.

    Attributes:
        template_name (str): Path to the template file to render ('home.html').

    Permissions:
        Public access - no authentication required.

    Context:
        The template receives the default Django TemplateView context,
        including request object and any additional context variables
        passed through get_context_data().

    Returns:
        HttpResponse: Renders the 'home.html' template with the application
            home page content.
    """
    template_name = 'home.html'
