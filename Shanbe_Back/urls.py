from django.contrib import admin
from django.urls import path, include
from django.views import generic
from drf_yasg.utils import swagger_auto_schema
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework.generics import GenericAPIView
from django.shortcuts import redirect

schema_view = get_schema_view(
   openapi.Info(
      title="Shanbe API",
      default_version='v1.0.0',
      description="Shanbe App - Daily planner",
      terms_of_service="",
      contact=openapi.Contact(email="contact@admernz.local"),
   ),
   public=True,
   permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    path('', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('tasks/', include('tasks.urls')),
    path('events/', include('events.urls')),
    path('calendar/', include('googlecalendar.urls')),
] 