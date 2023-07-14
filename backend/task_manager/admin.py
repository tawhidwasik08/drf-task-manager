from django.contrib import admin
from . import models

@admin.register(models.Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('task_id', 'task_name', 'task_description', 'task_due_date', 'task_creator', 'display_assignees', 'priority', 'created', 'modified')

    def display_assignees(self, obj):
        assignees = obj.task_assignee.all()
        return ", ".join([str(assignee) for assignee in assignees])
        
    display_assignees.short_description = 'Assignees'



@admin.register(models.TaskComment)
class TaskCommentAdmin(admin.ModelAdmin):
    list_display = ('comment_id', 'task_id', 'comment_creator', 'comment')
