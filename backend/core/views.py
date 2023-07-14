from json import JSONDecodeError
from .serializers import UserSerializer
from rest_framework.parsers import JSONParser
from rest_framework import status
from rest_framework.response import Response
from . models import UserProfile
from rest_framework.mixins import ListModelMixin
from rest_framework import viewsets, status
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticated, AllowAny
from . permissions import IsAdmin, IsManager
from rest_framework.exceptions import PermissionDenied
from rest_framework.serializers import ValidationError
from drf_yasg.utils import swagger_auto_schema
from . custom_schemas import *
from drf_yasg.inspectors import CoreAPICompatInspector

class NoSortSearchInspector(CoreAPICompatInspector):
    def get_filter_parameters(self, filter_backend):
        return []

class UserViewSet(ListModelMixin, viewsets.GenericViewSet):
        """
        Create or view user profile(s).
        
        list:
        Retrieve a list of user profiles.

        create:
        Create a new user profile.

        Attributes:
            parser_classes (list): The list of parser classes used for request parsing.
            queryset (QuerySet): The queryset of UserProfile objects.
            serializer_class (Serializer): The serializer class used for user profile serialization.
            pagination_class (Pagination): The pagination class used for user profile listing.
            http_method_names (list): The allowed HTTP methods for this ViewSet.

        """
        parser_classes = [JSONParser]
        queryset = UserProfile.objects.all()
        serializer_class = UserSerializer
        pagination_class = LimitOffsetPagination

        http_method_names = ['get', 'post']

        def get_permissions(self):
            """
            Retrieve the list of permissions for the current action.

            Returns the list of permissions based on the action being performed.
            If the action is 'list', returns IsAuthenticated permission.
            If the action is 'create', returns AllowAny permission.
            For other actions, delegates to the parent class for default permissions.

            Returns:
                list: List of permission classes for the current action.
            """
            if self.action == 'list':
                return [IsAuthenticated()]
            elif self.action == 'create':
                return [AllowAny()]
            else:
                return super().get_permissions()
        
        
        @swagger_auto_schema(
            responses={
                200: get_user_list_schema,
                403: error_403_schema,
            },
            manual_parameters=[
                openapi.Parameter('id', openapi.IN_QUERY, description='Search User by user_id.', type=openapi.TYPE_INTEGER),
                openapi.Parameter('tasks', openapi.IN_QUERY, description='Option to show associated tasks for each user.', type=openapi.TYPE_BOOLEAN),
            ],
            filter_inspectors=[NoSortSearchInspector],
            manual_operation=False,
            operation_description='Retrieve all user profiles or a single profile based on the provided user ID.',
        )
        def list(self, request, *args, **kwargs):
            """
            List user profiles.

            Retrieve all user profiles or a single profile based on the provided user ID.
            Pass 'id' as a query parameter to get a single profile.
            Pass 'tasks' as true to include associated tasks information.

            Args:
                request (HttpRequest): The request object.

            Returns:
                Response: Response object with serialized user data and the status code.

            Raises:
                ValidationError: If the requested user is not found.
                PermissionDenied: If the user is not authorized to view user information.
            """
            try:
                if IsAdmin().has_permission(request, self) or IsManager().has_permission(request, self):
                    user_id = request.query_params.get('id')
                    if user_id:
                        user = self.get_queryset().filter(id=user_id).first()
                        if not user:
                            raise ValidationError("User not found.")
                        else:
                            serializer = self.get_serializer(user)
                            return Response(serializer.data)
                    else:
                        queryset = self.get_queryset()
                else:
                    raise PermissionDenied("You are not authorized to view user information.")
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
            
        @swagger_auto_schema(
                request_body=create_user_request_schema,
                responses={
                    201: create_user_reponse_schema,
                }
        )
        def create(self, request):
            """
            Create a new user profile.

            Args:
                request (HttpRequest): The request object.

            Returns:
                Response: Response object with the serialized user data and the status code.

            Raises:
                ValidationError: If the serializer data is invalid.
                JSONDecodeError: If there is an error decoding JSON data in the request.
            """
            try:
                serializer = UserSerializer(data=request.data)
                if serializer.is_valid(raise_exception=True):
                    serializer.save()
                    return Response({"result": "success", "created_user": serializer.data, "status_code": status.HTTP_201_CREATED}, status=status.HTTP_201_CREATED)
                else:
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            except ValidationError as e:
                return Response({"result": "error", "message": str(e), "status_code": status.HTTP_400_BAD_REQUEST}, status=status.HTTP_400_BAD_REQUEST)
            except JSONDecodeError as e:
                return Response({"result": "error","message": str(e), "status_code": status.HTTP_400_BAD_REQUEST}, status= status.HTTP_400_BAD_REQUEST)
            except Exception as e:
                    return Response({"result": "error", "message": str(e), "status_code": status.HTTP_500_INTERNAL_SERVER_ERROR}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)