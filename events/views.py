from django.db.models.query import QuerySet
from django.shortcuts import render
from .serializers import Event_CreateSerializer, Event_GetSerializer, SessionSerializer, Event_SessionsSerializer, Event_DeleteSerializer, Event_EditSerializer, Event_SearchSerializer
from rest_framework import generics, status
from rest_framework.fields import empty
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated 
from .models import event, session
from django.db import connection


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


class DeleteEventsAPI(generics.GenericAPIView):
    serializer_class = Event_DeleteSerializer
    permission_classes = (IsAuthenticated,)
    def delete(self, request, *args, **kwargs):
        serializer = self.get_serializer(data = request.data)

        if serializer.is_valid():
            if ('event_token' in serializer.data):
                eventselect = event.objects.filter(userid = request.user.id , event_token = serializer.data['event_token']).first()
                try:
                    event.delete(eventselect)
                except Exception as e:
                    response = {
                        'message': 'Event not found.',
                    }
                    return Response(response)
            else:
                response = {
                    'message': 'event_token is required.',
                }
                return Response(response)
                
            response = {
                'status': 'success',
                'code': status.HTTP_200_OK,
                'message': 'Event deleted successfully',
                'data': []
            }
            return Response(response)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        


class EditEventsAPI(generics.UpdateAPIView):
    serializer_class = Event_EditSerializer
    permission_classes = (IsAuthenticated,)

    def update(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            if ('event_token' in serializer.data):
                event_editing = event.objects.filter(userid = request.user.id , event_token = serializer.data['event_token']).first()
            else:
                response = {
                    'message': 'event_token is required.',
                }
                return Response(response)

            if (event_editing == None):
                response = {
                    'message': 'Event not found.',
                }
                return Response(response)

            if(serializer.data.get("title") != None):
                event_editing.title = (serializer.data.get("title"))
            if(serializer.data.get("privacy") != None):
                event_editing.privacy = (serializer.data.get("privacy"))
            if(serializer.data.get("description") != None ):
                event_editing.description = (serializer.data.get("description"))
            if(serializer.data.get("category") != None ):
                event_editing.category = (serializer.data.get("category"))
            if(serializer.data.get("isVirtual") != None ):
                event_editing.isVirtual = (serializer.data.get("isVirtual"))
            if(serializer.data.get("location") != None ):
                event_editing.location = (serializer.data.get("location"))
            if(serializer.data.get("sessions") != None ):
                event_editing.sessions = (serializer.data.get("sessions"))
            
            event_editing.save()

            #print(serializer.data.get("sessions") , "5555555555")

            with connection.cursor() as cursor:
                cursor.execute("DELETE FROM events_session WHERE event_id = %s", [event_editing.id])

            temp_sessions = serializer.data.get("sessions")
            for se in temp_sessions:
                session_data = se.split("_")
                session_info ={'limit':session_data[0],'time':session_data[1]+"_"+session_data[2]}
                session.objects.create(event=event_editing, **session_info)

            response = {
                'status': 'success',
                'code': status.HTTP_200_OK,
                'message': 'Task updated successfully',
                'data': []
            }

            return Response(response)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class Event_SearchAPI(generics.GenericAPIView):
    serializer_class = Event_SearchSerializer
    permission_classes = (IsAuthenticated,)
    def post(self, request, *args, **kwargs):

        serializer = self.get_serializer(data = request.data)
        serializer.is_valid(raise_exception=True)

        templist = []

        if serializer.data.get("title") != None:
            with connection.cursor() as cursor:
                cursor.execute("SELECT id FROM `events` WHERE title LIKE %s", [serializer.data.get("title")])
                templist = cursor.fetchall()

        if serializer.data.get("privacy") != None:
            with connection.cursor() as cursor:
                cursor.execute("SELECT id FROM `events` WHERE privacy LIKE %s", [serializer.data.get("privacy")])
                templist = cursor.fetchall()

        if serializer.data.get("category") != None:
            with connection.cursor() as cursor:
                cursor.execute("SELECT id FROM `events` WHERE category LIKE %s", [serializer.data.get("category")])
                templist = cursor.fetchall()

        if serializer.data.get("isVirtual") != None:
            with connection.cursor() as cursor:
                cursor.execute("SELECT id FROM `events` WHERE isVirtual LIKE %s", [serializer.data.get("isVirtual")])
                templist = cursor.fetchall()

        if serializer.data.get("location") != None:
            with connection.cursor() as cursor:
                cursor.execute("SELECT id FROM `events` WHERE location LIKE %s", [serializer.data.get("location")])
                templist = cursor.fetchall()



        templist = list(templist)
        event_ids = []
        for i in templist:
            event_ids.append(i[0])
        
        events = event.objects.filter(id__in = event_ids)
        serializer = (self.get_serializer(events, many=True))

        # events = event.objects.filter(title = serializer.data.get("title"), privacy = serializer.data.get("privacy"),
        # category = serializer.data.get("category"), isVirtual = serializer.data.get("isVirtual"), location = serializer.data.get("location"))
        
        # serializer = (self.get_serializer(events, many=True))

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