from django.shortcuts import render
from .serializers import Event_CreateSerializer
from rest_framework import generics, status
from rest_framework.fields import empty
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated 

# Create your views here.
class EventsAPI(generics.GenericAPIView):
    serializer_class = Event_CreateSerializer
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        task = serializer.save()
        return Response({
        "task": Event_CreateSerializer(task, context=self.get_serializer_context()).data,
        })