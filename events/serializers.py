from django.db.models.base import Model
from rest_framework import fields, serializers
from django.contrib.auth.models import User
from rest_framework import viewsets
from rest_framework.fields import CharField
from .models import event, session

class SessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = session
        fields = ('id', 'session_token', 'event_id' , 'time', 'limit')

class Event_SessionsSerializer(serializers.ModelSerializer):

    session_set = SessionSerializer(many=True, read_only=True)
    first_name = serializers.SerializerMethodField('get_f_name')
    last_name = serializers.SerializerMethodField('get_l_name')
    username = serializers.SerializerMethodField('get_username')

    def get_f_name(self,obj):
        return self.context.get("f_name")

    def get_l_name(self,obj):
        return self.context.get("l_name")
        
    def get_username(self,obj):
        return self.context.get("username")

    class Meta:
        model = event
        fields = ('id', 'event_token', 'title', 'time', 'category', 'description',
         'location','session_set','first_name', 'last_name','username')
        extra_kwargs = {
            'event_token': {'required':False},
            'id': {'required':False},
            'title': {'required':False},
            'time': {'required':False},
            'status':{'required':False},
            'category': {'required':False},
            'description': {'required':False},
            'location': {'required':False},
        }

class Event_CreateSerializer(serializers.ModelSerializer):
    
    sessions = serializers.ListField(child = serializers.CharField(), write_only=True)

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
            #print (session_data)
            session_info ={'limit':session_data[0],'time':session_data[1]+"_"+session_data[2]}
            session.objects.create(event=e, **session_info)
        return e

class Event_EditSerializer(serializers.ModelSerializer):
    sessions = serializers.ListField(child=serializers.CharField()) #serializers.JSONField

    class Meta:
        model = event
        fields = ('id', 'user_token', 'event_token', 'title', 'privacy',
         'category', 'description', 'isVirtual', 'location' , 'sessions')
        extra_kwargs = {
            'user_token': {'read_only': True},
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
            'event_token': {'required':False},
            'id': {'required':False},
            'title': {'required':False},
            'time': {'required':False},
            'status':{'required':False},
            'category': {'required':False},
            'description': {'required':False},
            'location': {'required':False},
        }

class Event_SearchSerializer(serializers.ModelSerializer):

    s_time = serializers.CharField(required=False)

    class Meta:
        model = event
        fields = ('id', 'event_token', 'title', 'time', 's_time', 'privacy',
         'category', 'description', 'isVirtual', 'location')
        extra_kwargs = {
            'event_token': {'read_only': True, 'required':False},
            'id': {'read_only': True, 'required':False},
            'title': {'required':False},
            'time': {'required':False},
            'privacy': {'required':False},
            'category': {'required':False},
            'isVirtual': {'required':False},
            'description': {'read_only': True, 'required':False},
            'location': {'required':False},
        }

class Session_DeleteSerializer(serializers.ModelSerializer):
    class Meta:
        model = session
        fields = ('id', 'session_token')

class Session_GetSerializer(serializers.ModelSerializer):
    event = Event_GetSerializer( read_only=True)
    class Meta:
        model = session
        fields = ('id', 'session_token', 'limit', 'time', 'event')
        extra_kwargs = {
            'session_token': {'required':False},
            'id': {'required':False},
            'limit': {'required':False},
            'time': {'required':False},
            'status':{'required':False},
            'event': {'required':False},
        }

class Session_JoinSerializer(serializers.ModelSerializer):
    class Meta:
        model = session
        fields = ('id', 'session_token')
        extra_kwargs = {
            'session_token': {'required':True},
            'id': {'required':False},
        }

