from django.db import models
from django.contrib.auth import get_user_model
from django.db import models
from django.core.validators import MinValueValidator
from django.utils import timezone
from django_extensions.db.models import TimeStampedModel

class Task(TimeStampedModel, models.Model):
    """
    Represents a single task entry.

    Fields:
        task_id (AutoField): The unique identifier for the task.
        task_name (CharField): The name of the task.
        task_description (TextField): The description of the task.
        task_due_date (DateField): The due date of the task.
        task_creator (ForeignKey): The user who created the task.
        task_assignee (ManyToManyField): The users assigned to the task.
        priority (IntegerField): The priority level of the task.
        completed (BooleanField): Indicates if the task is completed or not.
    """
    class Meta:
        verbose_name = 'Task'
        verbose_name_plural = 'Tasks'
        ordering = ["task_id"]
    
    PRIORITY_CHOICES = (
            (1, 'High'),
            (2, 'Medium'),
            (3, 'Low'),
    )
    
    user = get_user_model()
    task_id = models.AutoField(primary_key=True)
    task_name = models.CharField(max_length=200, null=False, verbose_name="Task Name")
    task_description = models.TextField(null=True, blank=True, verbose_name="Task Description")
    task_due_date = models.DateField(null=True, blank=True, verbose_name="Due Date", validators=[MinValueValidator(timezone.now().date())])
    task_creator = models.ForeignKey(user, on_delete=models.CASCADE, null=False, default=None, related_name='task_creator', verbose_name="Task Creator")
    task_assignee = models.ManyToManyField(user, blank=True, default=None, related_name='task_assignees', verbose_name="Task Assignee(s)")
    priority = models.IntegerField(null=True, blank=True, choices=PRIORITY_CHOICES)
    completed = models.BooleanField(null=True, default=False, verbose_name="Completed")
    

    def __str__(self):
        return f'{self.task_name}'


class TaskComment(TimeStampedModel, models.Model):
    """
    Represents a comment on a task.

    Fields:
        comment_id (AutoField): The unique identifier for the comment.
        task (ForeignKey): The task to which the comment belongs.
        comment_creator (ForeignKey): The user who created the comment.
        comment (TextField): The content of the comment.
    """
    class Meta:
        verbose_name = 'Task Comment'
        verbose_name_plural = 'Task Comments'
        ordering = ["comment_id"]
    
    user = get_user_model()
    comment_id = models.AutoField(primary_key=True)
    task_id = models.ForeignKey(Task, on_delete=models.CASCADE, null=False, verbose_name="Task")
    comment_creator = models.ForeignKey(user, on_delete=models.CASCADE, null=False, default=None, related_name='comment_creator')
    comment = models.TextField(verbose_name="Comment")

    def __str__(self):
        return f'{self.comment}'