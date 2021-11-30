from django.shortcuts import render
from .serializers import Event_CreateSerializer, SessionSerializer
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
        event = serializer.save()
        return Response(request.data, status=status.HTTP_201_CREATED)

        #return Sessions(request, event)
def Sessions(request, event):
    
    for session in request.data.getlist('sessions'):
        print(session)
        data={'time':'sad','limit':'12','event_id':event.id}
        print(data)
        serializer = SessionSerializer(data = data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        response = {
                    'status': 'success',
                    'code': status.HTTP_200_OK,
                    'message': 'Password updated successfully',
                    'data': []
                }

        return Response(response)

class SessionsAPI(generics.GenericAPIView):
    serializer_class = SessionSerializer
    def post(self, request, *args, **kwargs):
        print("ll")