from django.contrib.auth.models import User
from django.db.models.query import QuerySet
from django.shortcuts import render

from accounts.models import Metadata
from .serializers import Event_CreateSerializer, Event_GetSerializer, Event_SessionsSerializer, Event_DeleteSerializer, Session_GetDaySerializer, Session_JoinSerializer, Session_UsersSerializer
from .serializers import Event_EditSerializer, Event_SearchSerializer, Session_DeleteSerializer, Session_GetSerializer
from rest_framework import generics, status
from rest_framework.fields import empty
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated 
from .models import event, session
from django.db import connection
from django.core.mail import send_mail  
from googlecalendar.GoogleCalendarInsert import insert

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
            return Response(response, status=status.HTTP_400_BAD_REQUEST)

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
                    return Response(response, status=status.HTTP_400_BAD_REQUEST)
            else:
                response = {
                    'message': 'event_token is required.',
                }
                return Response(response, status=status.HTTP_400_BAD_REQUEST)
                
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
                return Response(response, status=status.HTTP_400_BAD_REQUEST)

            if (event_editing == None):
                response = {
                    'message': 'Event not found.',
                }
                return Response(response, status=status.HTTP_400_BAD_REQUEST)

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
            if(serializer.data.get("link") != None ):
                event_editing.address = (serializer.data.get("link"))
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
                        return Response(response, status=status.HTTP_400_BAD_REQUEST)
                
                else:
                    response = {
                            'message': 'User not allowed.',
                        }
                    return Response(response, status=status.HTTP_400_BAD_REQUEST)

            else:
                response = {
                    'message': 'session_token is required.',
                }
                return Response(response, status=status.HTTP_400_BAD_REQUEST)
                
            response = {
                'status': 'success',
                'code': status.HTTP_200_OK,
                'message': 'Session deleted successfully',
                'data': []
            }
            return Response(response)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UsersSessionsAPI(generics.GenericAPIView):
    serializer_class = Session_UsersSerializer
    permission_classes = (IsAuthenticated,)
    def post(self, request, *args, **kwargs):
        if ('session_token' in request.data):
            sessionselect = session.objects.filter(session_token = request.data['session_token']).first()
            eventselect = sessionselect.event
            userselect = eventselect.userid
            if (userselect == request.user.id):

                try:
                    users = sessionselect.users.all()
                    serializer = (self.get_serializer(users, many=True))

                    return Response(serializer.data)

                except Exception as e:
                    response = {
                        'message': 'Session not found.',
                    }
                    return Response(response, status=status.HTTP_400_BAD_REQUEST)
            
            else:
                response = {
                        'message': 'User not allowed.',
                    }
                return Response(response, status=status.HTTP_400_BAD_REQUEST)

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
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
        
        if (sessionselect.filled >= sessionselect.limit):
            response = {
            'message': 'no space.',
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
        sessionselect.users.add(request.user)
        sessionselect.filled = sessionselect.filled + 1

        user = request.user
        try:
            metadata = user.metadata

        except Exception as e:
            metadata = Metadata(user=user)
            
        if (sessionselect.category == "Sport"):
            metadata.sport += 1
        if (sessionselect.category == "Study"):
            metadata.study += 1
        if (sessionselect.category == "Meeting"):
            metadata.meeting += 1
        if (sessionselect.category == "Work"):
            metadata.work += 1
        if (sessionselect.category == "hang out"):
            metadata.hangout += 1

        metadata.save()

        sessionselect.save()

        """Add to google calendar"""
        with connection.cursor() as cursor:
            cursor.execute("SELECT userid FROM google_calendar")
            userids = cursor.fetchall()
        userid_arr = []
        [userid_arr.append(id[0]) for id in userids if userid_arr.count != 0]
        #print(userid_arr)
        if request.user.id in userid_arr:
            with connection.cursor() as cursor:
                cursor.execute("SELECT access_token FROM google_calendar WHERE userid = %s", request.user.id)
                access_token = cursor.fetchone()
                cursor.execute("SELECT refresh_token FROM google_calendar WHERE userid = %s", request.user.id)
                refresh_token = cursor.fetchone()
                cursor.execute("SELECT event_id FROM events_session WHERE session_token = %s", serializer.data['session_token'])
                eventid = cursor.fetchone()
                cursor.execute("SELECT time FROM events_session WHERE session_token = %s", serializer.data['session_token'])
                session_time = cursor.fetchone()
                cursor.execute("SELECT title FROM events WHERE id = %s", eventid)
                event_title = cursor.fetchone()
                cursor.execute("SELECT description FROM events WHERE id = %s", eventid)
                event_description = cursor.fetchone()
            insert(access_token[0], refresh_token[0], event_title[0], event_description[0], session_time[0])

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
                return Response(response, status=status.HTTP_400_BAD_REQUEST)
            sessionselect.filled = sessionselect.filled - 1
            sessionselect.save()

            user = request.user
            try:
                metadata = user.metadata

            except Exception as e:
                metadata = Metadata(user=user)
                
            if (sessionselect.category == "Sport" and metadata.sport>0):
                metadata.sport -= 1
            if (sessionselect.category == "Study" and metadata.study>0):
                metadata.study -= 1
            if (sessionselect.category == "Meeting" and metadata.meeting>0):
                metadata.meeting -= 1
            if (sessionselect.category == "Work" and metadata.work>0):
                metadata.work -= 1
            if (sessionselect.category == "hang out" and metadata.hangout>0):
                metadata.hangout -= 1
            metadata.save()


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
            return Response(response, status=status.HTTP_400_BAD_REQUEST)


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
    serializer_class = Session_GetSerializer
    permission_classes = (IsAuthenticated,)
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data = request.data)
        serializer.is_valid(raise_exception=True)
        sessions = request.user.user_sessions.filter(time__startswith = serializer.data['time'])
        serializer = (self.get_serializer(sessions, many=True))
        return Response(serializer.data)



class GetEventsSuggestionAPI(generics.GenericAPIView):
    serializer_class = Event_GetSerializer
    permission_classes = (IsAuthenticated,)
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data = request.data)
        serializer.is_valid(raise_exception=True)
        user = request.user
        
        queryset = []

        user = request.user
        try :
            metadata = user.metadata
  
        except Exception as e:
            metadata = Metadata(user=user)
    
        if(metadata.city == "Not set"):
            events = event.objects.all()
        else :
            events = event.objects.filter(location = metadata.city)
        

        category_name = ["work", "sport", "study", "meeting", "hangout"]
        category_count = [metadata.work, metadata.sport, metadata.study, metadata.meeting, metadata.hangout]
        
        for i in range(4):
            for j in range(0, 4-i):
                if category_count[j] < category_count[j + 1] :
                    category_count[j], category_count[j + 1] = category_count[j + 1], category_count[j]
                    category_name[j], category_name[j + 1] = category_name[j + 1], category_name[j]
                    
        for i in range(5):
            if (category_name[i] == "sport"):
                q = events.filter(category = "sport")
            if (category_name[i] == "work"):
                q = events.filter(category = "work")
            if (category_name[i] == "meeting"):
                q = events.filter(category = "meeting")
            if (category_name[i] == "study"):
                q = events.filter(category = "study")
            if (category_name[i] == "hangout"):
                q = events.filter(category = "hangout")
            for x in q:
                queryset.append(x)

        serializer = (self.get_serializer(queryset, many=True))
        return Response(serializer.data)
