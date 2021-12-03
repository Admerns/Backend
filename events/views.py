from django.db.models.query import QuerySet
from django.shortcuts import render
from .serializers import Event_CreateSerializer, Event_GetSerializer, Event_SessionsSerializer, SessionSerializer
from rest_framework import generics, status
from rest_framework.fields import empty
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated 
from .models import event

# Create your views here.
class EventsAPI(generics.GenericAPIView):
    serializer_class = Event_CreateSerializer
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        event = serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class Event_SessionsAPI(generics.GenericAPIView):
    serializer_class = Event_SessionsSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        e = event.objects.filter(event_token = serializer.data['event_token']).first()
        serializer = (self.get_serializer(e))
        
        return Response(serializer.data, status=status.HTTP_200_OK)

class GetEventsAPI(generics.GenericAPIView):
    serializer_class = Event_GetSerializer
    def get(self, request, *args, **kwargs):
        serializer = self.get_serializer(data = request.data)
        serializer.is_valid(raise_exception=True)

        events = event.objects.all()
        
        serializer = (self.get_serializer(events, many=True))
        return Response(serializer.data)


        
# def Sessions(request, event):
    
#     for session in request.data.getlist('sessions'):
#         print(session)
#         data={'time':'sad','limit':'12','event_id':event.id}
#         print(data)
#         serializer = SessionSerializer(data = data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         response = {
#                     'status': 'success',
#                     'code': status.HTTP_200_OK,
#                     'message': 'Password updated successfully',
#                     'data': []
#                 }

#         return Response(response)

# class SessionsAPI(generics.GenericAPIView):
#     serializer_class = SessionSerializer
#     def post(self, request, *args, **kwargs):
#         print("ll")