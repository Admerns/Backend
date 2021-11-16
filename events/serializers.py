from django.db.models.base import Model
from rest_framework import fields, serializers
from django.contrib.auth.models import User
from rest_framework import viewsets
from rest_framework.fields import CharField
from .models import event

class Event_CreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = event
        fields = ('id', 'user_token', 'event_token', 'limit', 'title', 'time', 'privacy',
         'category', 'description', 'isVirtual', 'location')
        extra_kwargs = {
            'event_token': {'read_only': True},
            'time': {'required':False},
        }