from rest_framework import serializers
from . models import UserProfile
from task_manager.models import Task
from task_manager.serializers import TaskSerializer

class UserSerializer(serializers.ModelSerializer):
	"""
    Serializer class for User model.

    Inherits from ModelSerializer class.
    """
	# tasks = serializers.SerializerMethodField()
	user_id = serializers.IntegerField(source='id', required=False)

	class Meta:
		model = UserProfile
		fields = ['user_id', 'username', 'email', 'role', 'password', 'date_joined']
		# fields = ['user_id', 'username', 'email', 'role', 'password', 'date_joined', 'tasks']
		extra_kwargs = {
			'password': {'write_only': True}
		}
	
	
	def get_tasks(self, user):
		"""
		Retrieve the tasks associated with the user.

		Args:
			user (UserProfile): The user instance for which to retrieve tasks.

		Returns:
			dict: A dictionary containing the created tasks and assigned tasks for the user.
		"""
		created_tasks = Task.objects.filter(task_creator=user)
		assigned_tasks = Task.objects.filter(task_assignee=user)
		created_tasks_data = TaskSerializer(created_tasks, many=True).data
		assigned_tasks_data = TaskSerializer(assigned_tasks, many=True).data
		tasks = {
			'created_tasks': created_tasks_data,
			'assigned_tasks': assigned_tasks_data
		}
		return tasks

	# def to_representation(self, instance):
	# 	"""
    #     Convert the instance into a representation suitable for serialization. For the purpose
    #     of accessing tasks associated with each user optionally through parameter in request.

    #     Args:
    #         instance (UserProfile): The user instance to represent.

    #     Returns:
    #         dict: The serialized representation of the user instance, optionally excluding the 'tasks' field.
    #     """
	# 	request = self.context.get('request')
	# 	show_tasks = request and hasattr(request, 'query_params') and request.query_params.get('tasks', '').lower() == 'true'

	# 	data = super().to_representation(instance)
	# 	if not show_tasks:
	# 		data.pop('tasks', None)
	# 	return data
	