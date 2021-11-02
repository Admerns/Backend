from django.urls import path, include
from .views import TasksAPI

urlpatterns = [
    path('task_create/', TasksAPI.as_view(), name='task_create'),
]