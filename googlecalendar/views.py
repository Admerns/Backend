from django.contrib.auth.models import User
from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated 
from rest_framework.response import Response
from rest_framework import generics, status
from .serializers import GoogleCalendarLogin_CreateSerializer
# Create your views here.

class GoogleCalendarLoginAPI(generics.GenericAPIView):
    serializer_class = GoogleCalendarLogin_CreateSerializer
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        userid = request.user.id
        request.data['userid'] = userid
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)