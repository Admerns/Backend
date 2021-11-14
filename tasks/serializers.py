from enum import unique
from django.db.models.base import Model
from rest_framework import fields, serializers
from django.contrib.auth.models import User
from .models import task
from rest_framework import viewsets
from rest_framework.fields import CharField


class Task_CreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = task
        fields = ('id', 'user_token', 'task_token', 'title', 'time', 'status', 'category', 'description',
         'alarm_check', 'push_notification')
        extra_kwargs = {
            'task_token': {'read_only': True},
            'time': {'required':False},
        }

class Task_EditSerializer(serializers.ModelSerializer):
    class Meta:
        model = task
        fields = ('id', 'user_token', 'task_token', 'title', 'time', 'status', 'category', 'description',
         'alarm_check', 'push_notification')
        extra_kwargs = {
            'user_token': {'read_only': True},
            'title': {'required': False},
            'time': {'required': False},
            'status': {'required': False},
            'category': {'required': False},
            'description': {'required': False},
            'alarm_check': {'required': False},
            'push_notification': {'required': False}
        }

class Task_GetSerializer(serializers.ModelSerializer):
    class Meta:
        model = task
        fields = ('id', 'task_token', 'title', 'time', 'status', 'category', 'description',
         'alarm_check', 'push_notification')
        extra_kwargs = {
            'task_token': {'required':False},
            'id': {'required':False},
            'title': {'read_only': True, 'required':False},
            'time': {'read_only': True, 'required':False},
            'status':{'read_only': True, 'required':False},
            'category': {'read_only': True, 'required':False},
            'description': {'read_only': True, 'required':False},
            'alarm_check': {'read_only': True, 'required':False},
            'push_notification': {'read_only': True, 'required':False}
        }

class Task_FinishSerializer(serializers.ModelSerializer):
    status = CharField(max_length=10, required=True)
    class Meta:
        model = task
        fields = ('id', 'task_token' , 'status')
        

class Task_Get_DaySerializer(serializers.ModelSerializer):
    class Meta:
        model = task
        fields = ('id', 'task_token', 'title', 'time', 'status', 'category', 'description',
         'alarm_check', 'push_notification')
        extra_kwargs = {
            'task_token': {'required':False},
            'id': {'required':False},
            'title': {'read_only': True, 'required':False},
            'time': { 'required':False, 'required':False},
            'status':{'read_only': True, 'required':False},
            'category': {'read_only': True, 'required':False},
            'description': {'read_only': True, 'required':False},
            'alarm_check': {'required':False},
            'push_notification': {'read_only': True, 'required':False}
        }