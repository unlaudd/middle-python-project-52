"""
Status model for the statuses application.

This module defines the Status model, which represents task statuses
used to track the workflow state of tasks throughout their lifecycle.
Statuses are protected from deletion when associated with tasks to
maintain data integrity.
"""
from django.db import models
from django.utils.translation import gettext_lazy as _


class Status(models.Model):
    """
    Model representing a task status (e.g., 'New', 'In Progress', 'Done').
    
    Statuses define the workflow states that tasks can transition through.
    Each status has a unique name and tracks its creation timestamp.
    Statuses are protected from deletion when associated with tasks via
    the Task.status ForeignKey relationship (on_delete=models.PROTECT).

    Attributes:
        name (CharField): The display name of the status. Must be unique
            across all statuses. Maximum length is 100 characters.
        created_at (DateTimeField): Timestamp of when the status was created.
            Automatically set on creation and cannot be modified.

    Example:
        >>> status = Status.objects.create(name='In Progress')
        >>> status.name
        'In Progress'
        >>> task.status = status
        >>> task.save()

    Note:
        Attempting to delete a status that is associated with one or more
        tasks will raise a ProtectedError. This constraint ensures that
        task history and workflow integrity are maintained.
    """
    name = models.CharField(_('Name'), max_length=100, unique=True)
    created_at = models.DateTimeField(_('Created at'), auto_now_add=True)

    def __str__(self) -> str:
        """
        Return the string representation of the status.

        Returns:
            str: The status name.
        """
        return self.name
