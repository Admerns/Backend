from enum import unique
from django.db.models.base import Model
from rest_framework import fields, serializers
from django.contrib.auth.models import User
from .models import task
from rest_framework import viewsets


class Task_CreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = task
        fields = ('id', 'user_token', 'task_token', 'title', 'time', 'category', 'description',
         'alarm_check', 'push_notification')
        extra_kwargs = {'task_token': {'read_only': True}}