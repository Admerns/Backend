from django.urls import path, include

from .views import CancelSessionssAPI, DeleteSessionsAPI, EventsAPI, Event_SessionsAPI, GetCreatedEventsAPI, GetEventsAPI, DeleteEventsAPI, GetSessionsDayAPI, UsersSessionsAPI
from .views import EditEventsAPI, Event_SearchAPI, DeleteSessionsAPI, GetSessionssAPI,JoinSessionssAPI

urlpatterns = [
    path('create/', EventsAPI.as_view(), name='event-create'),
    path('get/', GetEventsAPI.as_view(), name='event-get'),
    path('created-get/', GetCreatedEventsAPI.as_view(), name='event-get'),
    path('enter-event-token/', Event_SessionsAPI.as_view(), name='enter-event-token'),
    path('delete/', DeleteEventsAPI.as_view(), name='event-delete'),
    path('edit/', EditEventsAPI.as_view(), name='event-edit'),
    path('search/', Event_SearchAPI.as_view(), name='event-search'),
    path('session-delete/', DeleteSessionsAPI.as_view(), name='session-delete'),
    path('session-get/', GetSessionssAPI.as_view(), name='session-get'),
    path('session-get-day/', GetSessionsDayAPI.as_view(), name='session-get-day'),
    path('session-join/', JoinSessionssAPI.as_view(), name='session-join'),
    path('session-cancel/', CancelSessionssAPI.as_view(), name='session-cancel'),
    path('session-users/', UsersSessionsAPI.as_view(), name='session-cancel'),
]
