from django.db.models.base import Model
from rest_framework import fields, serializers
from django.contrib.auth.models import User
from rest_framework import viewsets
from rest_framework.fields import CharField
from .models import google_calendar

class GoogleCalendarLogin_CreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = google_calendar
        fields = ('id', 'userid', 'access_token', 'refresh_token')
        # extra_kwargs = {
        #     'userid': {'read_only': True},
        # }

class Coordinates_CreateSerializer(serializers.Serializer):
    latitude = serializers.CharField()
    longitude = serializers.CharField()