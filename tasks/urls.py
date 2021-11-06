from django.urls import path, include
from .views import TasksAPI

urlpatterns = [
    path('task-create/', TasksAPI.as_view(), name='task-create'),
]