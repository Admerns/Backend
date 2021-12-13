from django.contrib.auth.models import User
from django.db.models.query import QuerySet
from django.shortcuts import render
from .serializers import Event_CreateSerializer, Event_GetSerializer, Event_SessionsSerializer, Event_DeleteSerializer, Session_GetDaySerializer, Session_JoinSerializer
from .serializers import Event_EditSerializer, Event_SearchSerializer, Session_DeleteSerializer, Session_GetSerializer
from rest_framework import generics, status
from rest_framework.fields import empty
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated 
from .models import event, session
from django.db import connection
from django.core.mail import send_mail  

# Create your views here.
class EventsAPI(generics.GenericAPIView):
    serializer_class = Event_CreateSerializer
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class Event_SessionsAPI(generics.GenericAPIView):
    serializer_class = Event_SessionsSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            e = event.objects.filter(event_token = serializer.data['event_token']).first()
            u = User.objects.filter(id = e.userid).first()
            serializer = (self.get_serializer(e, context={"f_name": u.first_name, "l_name": u.last_name, 'username':u.username}))
            
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            response = {
                'message': 'Event not found.',
            }
            return Response(response)

class GetEventsAPI(generics.GenericAPIView):
    serializer_class = Event_GetSerializer
    def get(self, request, *args, **kwargs):
        serializer = self.get_serializer(data = request.data)
        serializer.is_valid(raise_exception=True)

        events = event.objects.all()
        
        serializer = (self.get_serializer(events, many=True))
        return Response(serializer.data)

class GetCreatedEventsAPI(generics.GenericAPIView):
    serializer_class = Event_GetSerializer
    permission_classes = (IsAuthenticated,)
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data = request.data)
        serializer.is_valid(raise_exception=True)

        events = event.objects.filter(userid=request.user.id)
        
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
            if(serializer.data.get("address") != None ):
                event_editing.address = (serializer.data.get("address"))
            if(serializer.data.get("sessions") != None ):
                event_editing.sessions = (serializer.data.get("sessions"))
            
            event_editing.save()

            """dont delete"""
            # with connection.cursor() as cursor:   
            #     cursor.execute("DELETE FROM events_session WHERE event_id = %s", [event_editing.id])

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
    def post(self, request, *args, **kwargs):

        serializer = self.get_serializer(data = request.data)
        serializer.is_valid(raise_exception=True)

        _category = serializer.data.get("category")
        _location = serializer.data.get("location")
        _title = serializer.data.get("title")
        _time = serializer.data.get("s_time")
        _events = event.objects.filter(privacy=0)

        if _category:
            q = event.objects.filter(category=_category)
            _events = (_events&q)

        if _location:
            q = event.objects.filter(location=_location)
            _events = (_events&q)

        if _title:
            q = event.objects.filter(title=_title)
            _events = (_events&q)


        events = set()
        if _time:
            for e in _events:
                with connection.cursor() as cursor:
                    cursor.execute("SELECT id FROM `events_session` WHERE TRIM(SUBSTRING_INDEX(time,'_',1)) LIKE %s AND event_id LIKE %s",
                    [_time[:10], e.id])
                    templist = cursor.fetchall()

                templist = list(templist)
                session_ids = []
                for i in templist:
                    session_ids.append(i[0])

                sessions = session.objects.filter(id__in = session_ids)
                if sessions:
                    events.add(e)

            serializer = (self.get_serializer(events, many=True))

            return Response(serializer.data)
        
        serializer = (self.get_serializer(_events, many=True))

        return Response(serializer.data)

class DeleteSessionsAPI(generics.GenericAPIView):
    serializer_class = Session_DeleteSerializer
    permission_classes = (IsAuthenticated,)
    def delete(self, request, *args, **kwargs):
        serializer = self.get_serializer(data = request.data)

        if serializer.is_valid():
            if ('session_token' in serializer.data):
                sessionselect = session.objects.filter(session_token = serializer.data['session_token']).first()
                eventselect = sessionselect.event
                userselect = eventselect.userid
                if (userselect == request.user.id):

                    try:
                        users = sessionselect.users.all()
                        email_plaintext_message = "Event title: {title} \nSession time: {time}".format(title=eventselect.title , time=sessionselect.time)
                        for u in users:
                            
                            send_mail(
                                # title:
                                "Session delete alert for {title}".format(title="Shanbe App"),
                                # message:
                                ".یکی از ملاقات هایی که شما داشتید توسط سازنده رویداد لغو شده است \n .لطفا برای ثبت تاریخ ملاقات جدید مجددا اقدام کنید \n" + ":مشخصات رویداد لغو شده به شرح زیر است\n" + email_plaintext_message,
                                # from:
                                "noreply@shanbe.local",
                                # to:
                                [u.email]
                            )

                        session.delete(sessionselect)
                    except Exception as e:
                        response = {
                            'message': 'Session not found.',
                        }
                        return Response(response)
                
                else:
                    response = {
                            'message': 'User not allowed.',
                        }
                    return Response(response)

            else:
                response = {
                    'message': 'session_token is required.',
                }
                return Response(response)
                
            response = {
                'status': 'success',
                'code': status.HTTP_200_OK,
                'message': 'Session deleted successfully',
                'data': []
            }
            return Response(response)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class JoinSessionssAPI(generics.GenericAPIView):
    serializer_class = Session_JoinSerializer
    permission_classes = (IsAuthenticated,)
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        sessionselect = session.objects.filter(session_token = serializer.data['session_token']).first()
        if sessionselect.users.filter(id=request.user.id).exists():
            response = {
                'message': 'user already in session.',
            }
            return Response(response)
        
        if (sessionselect.filled >= sessionselect.limit):
            response = {
            'message': 'no space.',
            }
            return Response(response)
        sessionselect.users.add(request.user)
        sessionselect.filled = sessionselect.filled + 1
        sessionselect.save()
        response = {
                'status': 'success',
                'code': status.HTTP_200_OK,
                'message': 'joined session successfully',
                'data': []
            }
        return Response(response)


class CancelSessionssAPI(generics.GenericAPIView):
    serializer_class = Session_JoinSerializer
    permission_classes = (IsAuthenticated,)
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        sessionselect = session.objects.filter(session_token = serializer.data['session_token']).first()
        try :
            if (sessionselect.users.filter(id=request.user.id).exists()):
                sessionselect.users.remove(request.user)
            else:
                response = {
                    'message': 'user not in session.',
                }
                return Response(response)
            sessionselect.filled = sessionselect.filled - 1
            sessionselect.save()
            response = {
                    'status': 'success',
                    'code': status.HTTP_200_OK,
                    'message': 'canceled session successfully',
                    'data': []
                }
            return Response(response)
        except Exception as e:
            response = {
                'message': 'Session not found.',
            }
            return Response(response)


class GetSessionssAPI(generics.GenericAPIView):
    serializer_class = Session_GetSerializer
    permission_classes = (IsAuthenticated,)
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data = request.data)
        serializer.is_valid(raise_exception=True)

        sessions = request.user.user_sessions.all()
        serializer = (self.get_serializer(sessions, many=True))
        return Response(serializer.data)

class GetSessionsDayAPI(generics.GenericAPIView):
    serializer_class = Session_GetDaySerializer
    permission_classes = (IsAuthenticated,)
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data = request.data)
        serializer.is_valid(raise_exception=True)
        sessions = request.user.user_sessions.filter(time__startswith = serializer.data['time'])
        serializer = (self.get_serializer(sessions, many=True))
        return Response(serializer.data)