"""
Label model for the labels application.

This module defines the Label model, which represents task labels
used to categorize and organize tasks in the task management system.
"""
from django.db import models
from django.utils.translation import gettext_lazy as _


class Label(models.Model):
    """
    Model representing a task label (e.g., 'bug', 'feature', 'urgent').

    Labels are used to categorize and group tasks, providing a flexible
    tagging system that allows multiple labels per task. Each label has
    a unique name and tracks its creation timestamp.

    Attributes:
        name (CharField): The display name of the label. Must be unique
            across all labels. Maximum length is 50 characters.
        created_at (DateTimeField): Timestamp of when the label was created.
            Automatically set on creation and cannot be modified.

    Example:
        >>> label = Label.objects.create(name='bug')
        >>> label.name
        'bug'
        >>> task.labels.add(label)

    Note:
        Labels cannot be deleted if they are associated with any tasks.
        This constraint is enforced at the application level to maintain
        data integrity.
    """
    name = models.CharField(
        _('Name'),
        max_length=50,
        unique=True,
        help_text=_('Unique label name, maximum 50 characters.')
    )
    created_at = models.DateTimeField(
        _('Created at'),
        auto_now_add=True,
        help_text=_('Timestamp when the label was created.')
    )

    class Meta:
        """Meta options for the Label model."""
        verbose_name = _('label')
        verbose_name_plural = _('labels')
        ordering = ['name']

    def __str__(self) -> str:
        """
        Return the string representation of the label.

        Returns:
            str: The label name.
        """
        return self.name
