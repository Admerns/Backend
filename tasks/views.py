from django.shortcuts import render
from rest_framework import generics
from .serializers import Task_Create_Serializer
from rest_framework.response import Response

# Create your views here.
class TasksAPI(generics.GenericAPIView):
    serializer_class = Task_Create_Serializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        task = serializer.save()
        return Response({
        "task": Task_Create_Serializer(task, context=self.get_serializer_context()).data,
        })