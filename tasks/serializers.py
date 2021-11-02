from enum import unique
from django.db.models.base import Model
from rest_framework import fields, serializers
from django.contrib.auth.models import User
from .models import task
from rest_framework import viewsets


class Task_Create_Serializer(serializers.ModelSerializer):
    #user_id = serializers.CharField(source='auth_user.id')
    # user_id = User.objects.filter(username='james')
    class Meta:
        model = task
        fields = ('id', 'user_token', 'title', 'time', 'category', 'description',
         'alarm_check', 'push_notification')

# class GetRecordsByNameViewSet(viewsets.ViewSet):
#     def list(self, request, username):
#         accounts = Account.objects.filter(user__username=username)
#         accounts_to_return = AccountSerializer(accounts, many=True).data

#         return Response(accounts_to_return)
    

