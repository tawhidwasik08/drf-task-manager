from django.urls import path
from django.contrib import admin
from core import views as core_views
from task_manager import views as task_manager_views
from rest_framework import routers
from rest_framework.authtoken.views import obtain_auth_token
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework.permissions import AllowAny

# Swagger/OpenAPI schema view
schema_view = get_schema_view(
    openapi.Info(
        title="Task Manager API Documentation",
        default_version='v1',
        description="Documentation for the API endpoints for the Task Manager System Project.",
        contact=openapi.Contact(email="tawhidwasik08@gmail.com"),
        license=openapi.License(name="MIT License"),
    ),
    public=True,
    permission_classes=(AllowAny,),
)

router = routers.DefaultRouter()
router.register(r'users', core_views.UserViewSet, basename='task')
router.register(r'tasks', task_manager_views.TaskViewSet, basename='task')
router.register(r'task-comments', task_manager_views.TaskCommentViewSet, basename='task-comment')

urlpatterns = router.urls

urlpatterns += [
    path('admin/', admin.site.urls),
    # path('api-token-auth/', obtain_auth_token),
    # path('swagger<str:format>/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    # path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
