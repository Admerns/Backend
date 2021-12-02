from django.db.models.base import Model
from rest_framework import fields, serializers
from django.contrib.auth.models import User
from rest_framework import viewsets
from rest_framework.fields import CharField
from .models import event, session

class SessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = session
        fields = ('id', 'event_id' , 'time', 'limit')

class Event_EnterSerializer(serializers.ModelSerializer):
    class Meta:
        model = event
        fields = ('id', 'event_token')

class Event_CreateSerializer(serializers.ModelSerializer):
    
    sessions = serializers.ListField(child = serializers.CharField())

    class Meta:
        
        model = event
        fields = ('id', 'user_token', 'event_token', 'title', 'time', 'privacy',
         'category', 'description', 'isVirtual', 'location' , 'sessions')
        extra_kwargs = {
            'event_token': {'read_only': True},
            'time': {'required':False},
        }

    def create(self, validated_data):
        print (validated_data)
        sessions_data = validated_data.pop('sessions')
        e = event.objects.create(**validated_data)
        for session_data in sessions_data:
            session_data = session_data.split("_")
            print (session_data)
            session_info ={'limit':session_data[0],'time':session_data[1]+"_"+session_data[2]}
            session.objects.create(event=e, **session_info)
        return e

    def get_sessions(self, data):
        return data.pop('sessions')

class Event_EditSerializer(serializers.ModelSerializer):
    sessions = serializers.ListField(child=serializers.CharField()) #serializers.JSONField

    class Meta:
        
        model = event
        fields = ('id', 'user_token', 'event_token', 'title', 'privacy',
         'category', 'description', 'isVirtual', 'location' , 'sessions')
        extra_kwargs = {
            'event_token': {'read_only': True},
            'title': {'required':False},
            'privacy': {'required':False},
            'category': {'required':False},
            'description': {'required':False},
            'isVirtual': {'required':False},
            'location': {'required':False},
            'sessions': {'required':False}
        }

class Event_DeleteSerializer(serializers.ModelSerializer):
    class Meta:
        model = event
        fields = ('id', 'event_token')

class Event_GetSerializer(serializers.ModelSerializer):
    class Meta:
        model = event
        fields = ('id', 'event_token', 'title', 'time', 'category', 'description',
         'location')
        extra_kwargs = {
            'event_token': {'read_only': True, 'required':False},
            'id': {'required':False},
            'title': {'read_only': True, 'required':False},
            'time': {'read_only': True, 'required':False},
            'status':{'read_only': True, 'required':False},
            'category': {'read_only': True, 'required':False},
            'description': {'read_only': True, 'required':False},
            'location': {'read_only': True, 'required':False},
        }
        