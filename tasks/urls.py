from django.conf.urls import url
from django.urls import path, include
from .views import TasksAPI,TaskReadView

urlpatterns = [
    path('task-create/', TasksAPI.as_view(), name='task-create'),
    path('task-read/<int:pk>/', TaskReadView.as_view(),name='task-read'),
]