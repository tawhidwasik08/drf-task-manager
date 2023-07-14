from collections import OrderedDict
from .models import Task , TaskComment
from core.models import UserProfile
from rest_framework_json_api import serializers
from rest_framework import status
from rest_framework.exceptions import APIException
from django.contrib.auth import get_user_model

class TaskSerializer(serializers.ModelSerializer):
    """
    Serializer for the Task model.

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

    priority = serializers.ChoiceField(choices=Task.PRIORITY_CHOICES, required=False)
    task_assignee = serializers.PrimaryKeyRelatedField(queryset=get_user_model().objects.all(), many=True, required=False)

    class Meta:
        model = Task
        fields = '__all__'


class TaskCommentSerializer(serializers.ModelSerializer):
    """
    Serializer for the TaskComment model.

    Fields:
        comment_id (AutoField): The unique identifier for the comment.
        task_id (ForeignKey): The task to which the comment belongs.
        comment_creator (ForeignKey): The user who created the comment.
        comment (TextField): The content of the comment.
    """
    task_id = serializers.PrimaryKeyRelatedField(queryset=Task.objects.all(), required=False)

    class Meta:
        model = TaskComment
        fields = '__all__'