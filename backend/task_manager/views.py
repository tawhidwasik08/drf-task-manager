from json import JSONDecodeError
from django.http import JsonResponse
from .serializers import TaskSerializer, TaskCommentSerializer
from .models import Task , TaskComment
from rest_framework.parsers import JSONParser
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.mixins import ListModelMixin,UpdateModelMixin,RetrieveModelMixin, DestroyModelMixin
from .permissions import IsAdmin, IsManager, IsTeamMember
from rest_framework.exceptions import PermissionDenied
from django.contrib.auth import get_user_model
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.serializers import ValidationError
from django.http import Http404
from drf_yasg.utils import swagger_auto_schema
from . custom_schemas import *
from drf_yasg.inspectors import CoreAPICompatInspector

class NoSortSearchInspector(CoreAPICompatInspector):
    def get_filter_parameters(self, filter_backend):
        return []

class TaskViewSet(
    ListModelMixin,
    RetrieveModelMixin,
    UpdateModelMixin,
    DestroyModelMixin,
    viewsets.GenericViewSet,
):
    """
    A ViewSet for creating, retrieving, updating, and deleting tasks.

    retrieve: Retrieve the details of a specific task.

    list: Retrieve a list of tasks.

    partial_update: Partially / completely update a specific task.

    destroy: Delete a specific task.

    create: Create a new task.

    Attributes:
        permission_classes (list): The list of permission classes applied to this ViewSet.
        parser_classes (list): The list of parser classes used for request parsing.
        queryset (QuerySet): The queryset of Task objects.
        serializer_class (Serializer): The serializer class used for task serialization.
        pagination_class (Pagination): The pagination class used for task listing.
        http_method_names (list): The allowed HTTP methods for this ViewSet.
    
    """

    permission_classes = [IsAuthenticated, (IsAdmin | IsManager | IsTeamMember)]
    parser_classes = [JSONParser]
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    pagination_class = LimitOffsetPagination
    http_method_names = ['get', 'post', 'patch', 'delete']

    def is_user_allowed_delete(self, user, instance):
        """
        Check if the user is allowed to delete the task.

        Args:
            user (User): The user object.
            instance (Task): The task instance.

        Returns:
            bool: True if the user is allowed to delete the task, False otherwise.
        """
        task_creator_id = instance.task_creator.id
        if user.id == task_creator_id and (user.role == "admin" or user.role == "manager"):
            return True
        else:
            return False

    @swagger_auto_schema(
              responses={
                200: get_task_response_schema,
            },
        manual_parameters=[
                openapi.Parameter('completed', openapi.IN_QUERY, description='Is task completed', type=openapi.TYPE_BOOLEAN),
                openapi.Parameter('task_assignee_id', openapi.IN_QUERY, description='Search by task assignee id', type=openapi.TYPE_INTEGER),
                openapi.Parameter('due_date', openapi.IN_QUERY, description='Search by due date[Format: 2023-12-30 (YYYY-MM-DD)]', type=openapi.TYPE_STRING),
                openapi.Parameter('sort_by', openapi.IN_QUERY, description='Sort by [Option: due_date, id, priority] ', type=openapi.TYPE_STRING),
                openapi.Parameter('sort_dir', openapi.IN_QUERY, description='Direction of sort [Option: desc, asc]', type=openapi.TYPE_STRING),

            ],
            filter_inspectors=[NoSortSearchInspector],
            manual_operation=False,
            operation_description='Retrieve all tasks.'
        )
    def list(self, request, *args, **kwargs):
        """
        Retrieve a list of tasks.

        Args:
            request (Request): The HTTP request object.

        Returns:
            Response: The HTTP response containing the list of tasks.

        Raises:
            ValidationError: If the requested user is not found.
            PermissionDenied: If the user is not authorized to view user information.
        """
        user = request.user
        try:
            if IsAdmin().has_permission(request, self):
                queryset = self.get_queryset()  # All tasks for admin
            elif IsManager().has_permission(request, self):
                queryset = self.get_queryset().filter(task_creator=user)  # Tasks created by manager
            elif IsTeamMember().has_permission(request, self):
                queryset = self.get_queryset().filter(task_assignee=user)  # Tasks assigned to team member
            else:
                queryset = Task.objects.none()  
            
            completed = self.request.query_params.get('completed')
            task_assignee_id = self.request.query_params.get('task_assignee_id')
            due_date = self.request.query_params.get('due_date', None)
            sort_by = self.request.query_params.get('sort_by', None)
            sort_dir = request.query_params.get('sort_dir')

            # Apply additional filters based on query parameters
            if completed is not None:
                completed = str(completed).lower() == 'true'
                queryset = queryset.filter(completed=completed)
            
            if task_assignee_id:
                User = get_user_model()
                task_assignee = User.objects.get(id=task_assignee_id)
                queryset = queryset.filter(task_assignee=task_assignee)
            
            if due_date is not None:
                queryset = queryset.filter(task_due_date=due_date)

            if sort_by == 'due_date':
                if sort_dir == "desc":
                    queryset = queryset.order_by('task_due_date').reverse()
                else:
                    queryset = queryset.order_by('task_due_date')

            if sort_by == 'id':
                if sort_dir == "desc":
                    queryset = queryset.order_by('task_id').reverse()
                else:
                    queryset = queryset.order_by('task_id')
            
            if sort_by == 'priority':
                if sort_dir == "desc":
                    queryset = queryset.order_by('priority').reverse()
                else:
                    queryset = queryset.order_by('priority')
            
            
            page = self.paginate_queryset(queryset)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)

        except ValidationError as e:
            return Response({"result": "error", "message": str(e), "status_code": status.HTTP_400_BAD_REQUEST}, status=status.HTTP_400_BAD_REQUEST)
        except PermissionDenied as e:
            return Response({"result": "error", "message": str(e), "status_code": status.HTTP_403_FORBIDDEN}, status=status.HTTP_403_FORBIDDEN)
        except Exception as e:
            return Response({"result": "error", "message": str(e), "status_code": status.HTTP_500_INTERNAL_SERVER_ERROR}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    @swagger_auto_schema(responses={
                200: get_task_response_schema,
            },
        operation_description="Retrieve a task by id"
        )
    def retrieve(self, request, *args, **kwargs):
         return super().retrieve(request, *args, **kwargs)
         

    @swagger_auto_schema(
              request_body=patch_task_request_schema,
              responses={
                200: get_task_response_schema,
            },
        operation_description="Create a new task by id"
        )
    def create(self, request):
        """
        Create a new task.

        Args:
            request (Request): The HTTP request object.

        Returns:
            Response: The HTTP response containing the result of the operation.

        Raises:
            ValidationError: If the data provided in the request is invalid.
            JSONDecodeError: If there is an error decoding the JSON data.
            PermissionDenied: If the user is not authorized to create a task.
            Exception: If an unexpected error occurs.
        """
        try:
            serializer = TaskSerializer(data=request.data)
            if IsAdmin().has_permission(request, self) or IsManager().has_permission(request, self):
                if serializer.is_valid(raise_exception=True):
                    serializer.save(task_creator=self.request.user)
                    return Response({"result": "success", "created_task": serializer.data, "status_code": status.HTTP_201_CREATED}, status=status.HTTP_201_CREATED)
                else:
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            else:
                raise PermissionDenied("You are not authorized to create any task.")
        except ValidationError as e:
                return Response({"result": "error", "message": str(e), "status_code": status.HTTP_400_BAD_REQUEST}, status=status.HTTP_400_BAD_REQUEST)
        except JSONDecodeError as e:
                return JsonResponse({"result": "error","message": str(e), "status_code": status.HTTP_400_BAD_REQUEST}, status= status.HTTP_400_BAD_REQUEST)
        except PermissionDenied as e:
                return JsonResponse({"result": "error", "message": str(e), "status_code": status.HTTP_403_FORBIDDEN}, status=status.HTTP_403_FORBIDDEN)
        except Exception as e:
                    return Response({"result": "error", "message": str(e), "status_code": status.HTTP_500_INTERNAL_SERVER_ERROR}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    @swagger_auto_schema(
              request_body=patch_task_request_schema,
              responses={
                200: patch_task_update_response_schema,
            },
        operation_description="Update a task by id"
    )
    def partial_update(self, request, *args, **kwargs):
        """
        Update a task.

        Args:
            request (Request): The HTTP request object.

        Returns:
            Response: The HTTP response containing the updated task data.

        Raises:
            JSONDecodeError: If there is an error decoding JSON data.
            PermissionDenied: If the user is not authorized to update the task.
            Http404: If the requested task does not exist.
            Exception: If an unexpected error occurs.
        """
        try:
            partial = kwargs.pop('partial', False)
            instance = self.get_object()
            serializer = self.get_serializer(instance, data=request.data, partial=partial)
            if serializer.is_valid(raise_exception=True):
                self.perform_update(serializer)
                return Response({"result": "success", "updated_task": serializer.data, "status_code": status.HTTP_200_OK}, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except ValidationError as e:
                return Response({"result": "error", "message": str(e), "status_code": status.HTTP_400_BAD_REQUEST}, status=status.HTTP_400_BAD_REQUEST)
        except JSONDecodeError as e :
            return JsonResponse({"result": "error","message": str(e), "status_code": status.HTTP_400_BAD_REQUEST}, status=status.HTTP_400_BAD_REQUEST)
        except PermissionDenied:
            return Response({"result": "error", "message": str(e), "status_code": status.HTTP_403_FORBIDDEN}, status=status.HTTP_403_FORBIDDEN)
        except Exception as e:
            return Response({"result": "error", "message": str(e), "status_code": status.HTTP_500_INTERNAL_SERVER_ERROR}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def destroy(self, request, *args, **kwargs):
        """
        Delete a task.

        Args:
            request (Request): The HTTP request object.

        Returns:
            Response: The HTTP response indicating the success of the deletion.

        Raises:
            PermissionDenied: If the user is not authorized to delete the task.
            Http404: If the requested task does not exist.
            Exception: If an unexpected error occurs.
        """
        try:
            instance = self.get_object()
            if self.is_user_allowed_delete(request.user, instance): 
                response_data = {'deleted_task_id': instance.task_id,'deleted_by': request.user.username}
                self.perform_destroy(instance)
                return Response({"result": "success", "deleted_task": response_data, "status_code": status.HTTP_200_OK}, status=status.HTTP_200_OK)
            else:
                raise PermissionDenied("You are not authorized to delete this task.")
        except PermissionDenied:
            return Response({"result": "error", "message": str(e), "status_code": status.HTTP_403_FORBIDDEN}, status=status.HTTP_403_FORBIDDEN)
        except Http404 as e:
            return Response({"result": "error", "message": str(e), "status_code": status.HTTP_404_NOT_FOUND}, status=status.HTTP_404_NOT_FOUND)            
        except Exception as e:
            return Response({"result": "error", "message": str(e), "status_code": status.HTTP_500_INTERNAL_SERVER_ERROR}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

class TaskCommentViewSet(
        ListModelMixin,
        RetrieveModelMixin,
        UpdateModelMixin,
        DestroyModelMixin,
        viewsets.GenericViewSet
):
    
    """
    A ViewSet for listing, creating, updating, and deleting Task Comments.

    retrieve: Retrieve the details of a specific task comment.

    list: Retrieve a list of task comments.

    partial_update: Partially / completely update a specific task comment.

    destroy: Delete a specific task comment.

    create: Create a new task comment.

    Attributes:
        permission_classes (list): The list of permission classes applied to this ViewSet.
        parser_classes (list): The list of parser classes used for request parsing.
        queryset (QuerySet): The queryset of TaskComment objects.
        serializer_class (Serializer): The serializer class used for task comment serialization.
        pagination_class (Pagination): The pagination class used for task comment listing.
        http_method_names (list): The allowed HTTP methods for this ViewSet.
    """
    permission_classes = [IsAuthenticated, (IsAdmin | IsManager | IsTeamMember)]
    parser_classes = [JSONParser]
    queryset = TaskComment.objects.all()
    serializer_class = TaskCommentSerializer
    pagination_class = LimitOffsetPagination

    http_method_names = ['get', 'post', 'patch', 'delete']

    def is_user_allowed_comment(self, user, task):
        """
        Checks if a user is allowed to comment on a task.
        Admins, Task Creator and Task Assigness are only allowed.

        Args:
            user (User): The user object.
            task (Task): The task object.

        Returns:
            bool: True if the user is allowed to comment, False otherwise.
        """
        if user.role == "admin" or task.task_creator == user and user.role == "manager" or user in task.task_assignee.all():
            return True
        else:
            return False

    def is_user_allowed_comment_delete(self, user, instance):
        """
        Checks if a user is allowed to delete a comment.
        Original commenter and admin is allowed to delete.

        Args:
            user (User): The user object.
            instance (TaskComment): The comment instance.

        Returns:
            bool: True if the user is allowed to delete the comment, False otherwise.
        """
        comment_creator_id = instance.comment_creator.id
        if user.id == comment_creator_id or user.role == "admin":
            return True
        else:
            return False
        
    @swagger_auto_schema(
              responses={
                200: get_task_comment_response_schema,
            },
            filter_inspectors=[NoSortSearchInspector],
            manual_operation=False,
            operation_description='Retrieve all task comments.'
        )
    def list(self, request, *args, **kwargs):
        """
        Retrieve a list of task comments based on the user's role.

        Args:
            request (Request): The request object.

        Returns:
            Response: The response containing the serialized task comments.
        """
        user = request.user
        try:
            if IsAdmin().has_permission(request, self):
                queryset = self.get_queryset()  # All task comment for admin
            elif IsManager().has_permission(request, self):
                queryset = self.get_queryset().filter(comment_creator=user)  # Tasks created by manager
            elif IsTeamMember().has_permission(request, self):
                queryset = self.get_queryset().filter(comment_creator=user)  # Tasks assigned to team member
            else:
                queryset = Task.objects.none()  
            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data)
        except ValidationError as e:
                return Response({"result": "error", "message": str(e), "status_code": status.HTTP_400_BAD_REQUEST}, status=status.HTTP_400_BAD_REQUEST)
        except PermissionDenied as e:
            return JsonResponse({"result": "error", "message": str(e), "status_code": status.HTTP_403_FORBIDDEN}, status=status.HTTP_403_FORBIDDEN)
        except Exception as e:
            return JsonResponse({"result": "error", "message": str(e), "status_code": status.HTTP_500_INTERNAL_SERVER_ERROR}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @swagger_auto_schema(
              responses={
                200: get_task_comment_response_schema,
            },
        operation_description="Retrieve a task comment by id."
        )
    def retrieve(self, request, *args, **kwargs):
         return super().retrieve(request, *args, **kwargs)
    

    @swagger_auto_schema(
              request_body=post_task_comment_request_schema,
              responses={
                200: post_task_comment_response_schema,
            },
        operation_description="Create a task comment for a task."
        )
    def create(self, request):
        """
        Create a new task comment.

        Args:
            request (Request): The request object.

        Returns:
            Response: The response indicating the success or failure of the comment creation.
        """
        try:
            serializer = TaskCommentSerializer(data=request.data)
            if serializer.is_valid(raise_exception=True):
                task_id = request.data.get('task_id')
                task = Task.objects.get(task_id=task_id)
                if self.is_user_allowed_comment(self.request.user, task):
                    serializer.save(comment_creator=self.request.user)
                    return Response({"result": "success", "created_task_comment": serializer.data, "status_code": status.HTTP_201_CREATED}, status=status.HTTP_201_CREATED)
                else:
                    raise PermissionDenied("You are not authorized to comment on this task.")
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except ValidationError as e:
                return Response({"result": "error", "message": str(e), "status_code": status.HTTP_400_BAD_REQUEST}, status=status.HTTP_400_BAD_REQUEST)
        except JSONDecodeError as e:
                return JsonResponse({"result": "error","message": str(e), "status_code": status.HTTP_400_BAD_REQUEST}, status= status.HTTP_400_BAD_REQUEST)
        except Exception as e:
                    return Response({"result": "error", "message": str(e), "status_code": status.HTTP_500_INTERNAL_SERVER_ERROR}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    @swagger_auto_schema(
              request_body = patch_task_comment_request_schema,
              responses={
                200: post_task_comment_response_schema,
            },
        operation_description="Update a task comment for a task."
        )
    def partial_update(self, request, *args, **kwargs):
        """
        Update a task comment.

        Args:
            request (Request): The request object.

        Returns:
            Response: The response indicating the success or failure of the comment update.
        """
        try:
            partial = kwargs.pop('partial', False)
            instance = self.get_object()
            serializer = self.get_serializer(instance, data=request.data, partial=partial)
            if serializer.is_valid(raise_exception=True):
                comment_creator_id = instance.comment_creator.id
                updater_id = self.request.user.id
                if comment_creator_id == updater_id:
                    self.perform_update(serializer)
                    return Response(serializer.data, status=status.HTTP_200_OK)
                else:
                    raise PermissionDenied("You are not authorized to update this task comment.") 
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except ValidationError as e:
            return Response({"result": "error", "message": str(e), "status_code": status.HTTP_400_BAD_REQUEST}, status=status.HTTP_400_BAD_REQUEST)
        except JSONDecodeError as e :
            return JsonResponse({"result": "error","message": str(e), "status_code": status.HTTP_400_BAD_REQUEST}, status=status.HTTP_400_BAD_REQUEST)
        except PermissionDenied:
            return Response({"result": "error", "message": str(e), "status_code": status.HTTP_403_FORBIDDEN}, status=status.HTTP_403_FORBIDDEN)
        except Exception as e:
            return Response({"result": "error", "message": str(e), "status_code": status.HTTP_500_INTERNAL_SERVER_ERROR}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    @swagger_auto_schema(
        operation_description="Delete a task comment by id. Only possible by comment creator or admin."
    )
    def destroy(self, request, *args, **kwargs):
        """
        Delete a task comment.

        Args:
            request (Request): The request object.

        Returns:
            Response: The response indicating the success or failure of the comment deletion.

        Raises:
            PermissionDenied: If the user is not authorized to delete the task comment.
        """
        try:
            instance = self.get_object()
            if self.is_user_allowed_comment_delete(request.user, instance): 
                response_data = {
                    'message': 'Task comment successfully deleted.',
                    'deleted_comment': instance.comment,
                    'deleted_by': request.user.username
                }
                self.perform_destroy(instance)
                return Response(response_data, status=status.HTTP_200_OK)
            else:
                raise PermissionDenied("You are not authorized to delete this task comment.")
        except PermissionDenied as e:
            return Response({"result": "error", "message": str(e), "status_code": status.HTTP_403_FORBIDDEN}, status=status.HTTP_403_FORBIDDEN)
        except Http404 as e:
            return Response({"result": "error", "message": str(e), "status_code": status.HTTP_404_NOT_FOUND}, status=status.HTTP_404_NOT_FOUND)            
        except Exception as e:
            return Response({"result": "error", "message": str(e), "status_code": status.HTTP_500_INTERNAL_SERVER_ERROR}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        
        