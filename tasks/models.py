"""
Task and Label models for the tasks application.

This module defines the core models for task management:
- Label: A categorization tag that can be attached to multiple tasks.
- Task: The primary entity representing work items with status, author,
  assignee, and associated labels.

These models implement the business logic for task tracking, including
protection rules that prevent deletion of referenced entities.
"""
from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _


class Label(models.Model):
    """
    Model representing a task label.

    Labels are used to categorize and group tasks (e.g., 'bug', 'feature',
    'urgent'). A single label can be associated with multiple tasks through
    a many-to-many relationship defined in the Task model.

    Attributes:
        name (CharField): The display name of the label. Must be unique
            across all labels. Maximum length is 50 characters.

    Example:
        >>> bug_label = Label.objects.create(name='bug')
        >>> feature_label = Label.objects.create(name='feature')
        >>> task.labels.add(bug_label, feature_label)

    Note:
        Labels are protected from deletion when associated with tasks.
        Attempting to delete a label that is linked to one or more tasks
        will raise a ProtectedError to maintain data integrity.
    """
    name = models.CharField(_('Name'), max_length=50, unique=True)

    def __str__(self):
        """
        Return the string representation of the label.

        Returns:
            str: The label name.
        """
        return self.name


class Task(models.Model):
    """
    Model representing a task in the task management system.

    Tasks are the primary work units that track progress through various
    statuses. Each task has a name, optional description, status, author,
    optional assignee, and can be associated with multiple labels.

    Attributes:
        name (CharField): The task title. Must be unique across all tasks.
            Maximum length is 100 characters.
        description (TextField): Optional detailed description of the task.
            Can be blank.
        status (ForeignKey): The current workflow status of the task.
            Protected from deletion (on_delete=PROTECT) — cannot delete
            a status if tasks reference it.
        author (ForeignKey): The user who created the task. Protected from
            deletion (on_delete=PROTECT) — cannot delete a user if they
            authored tasks.
        assignee (ForeignKey): The user responsible for completing the task.
            Optional (null=True, blank=True). Set to NULL on user deletion
            (on_delete=SET_NULL) — tasks remain but lose their assignee.
        labels (ManyToManyField): Labels associated with the task. Optional
            (blank=True). A task can have zero or more labels, and a label
            can be associated with zero or more tasks.
        created_at (DateTimeField): Timestamp of when the task was created.
            Automatically set on creation and cannot be modified.

    Example:
        >>> from django.contrib.auth.models import User
        >>> from statuses.models import Status
        >>>
        >>> status = Status.objects.get(name='New')
        >>> author = User.objects.get(username='john')
        >>> task = Task.objects.create(
        ...     name='Fix login bug',
        ...     description='Users cannot log in with special characters',
        ...     status=status,
        ...     author=author
        ... )
        >>> bug_label = Label.objects.get(name='bug')
        >>> task.labels.add(bug_label)

    Relationships:
        - Task -> Status: Many-to-one (multiple tasks can have the same status)
        - Task -> User (author): Many-to-one (one user can author many tasks)
        - Task -> User (assignee): Many-to-one, optional (one user can be
          assigned many tasks)
        - Task -> Label: Many-to-many (tasks and labels have bidirectional
          many-to-many relationship)

    Deletion Behavior:
        - Cannot delete a Status if tasks reference it (ProtectedError)
        - Cannot delete a User if they authored tasks (ProtectedError)
        - Deleting a User who is an assignee sets assignee to NULL (tasks
          remain but become unassigned)
        - Deleting a Label that is associated with tasks raises ProtectedError
    """
    name = models.CharField(_('Name'), max_length=100, unique=True)
    description = models.TextField(_('Description'), blank=True)
    status = models.ForeignKey(
        'statuses.Status', 
        on_delete=models.PROTECT, 
        verbose_name=_('Status')
    )
    author = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name='authored_tasks',
        verbose_name=_('Author')
    )
    assignee = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='assigned_tasks',
        verbose_name=_('Assignee')
    )
    labels = models.ManyToManyField(
        'labels.Label',
        blank=True,
        verbose_name=_('Labels')
    )
    created_at = models.DateTimeField(_('Created at'), auto_now_add=True)

    def __str__(self):
        """
        Return the string representation of the task.

        Returns:
            str: The task name.
        """
        return self.name
