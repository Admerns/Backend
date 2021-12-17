from django.urls import path, include
from .views import CancelSessionssAPI, DeleteSessionsAPI, EventsAPI, Event_SessionsAPI, GetCreatedEventsAPI, GetEventsAPI, DeleteEventsAPI, GetSessionsDayAPI
from .views import EditEventsAPI, Event_SearchAPI, DeleteSessionsAPI, GetSessionssAPI,JoinSessionssAPI

urlpatterns = [
    path('event-create/', EventsAPI.as_view(), name='event-create'),
    path('event-get/', GetEventsAPI.as_view(), name='event-get'),
    path('event-created-get/', GetCreatedEventsAPI.as_view(), name='event-get'),
    path('enter-event-token/', Event_SessionsAPI.as_view(), name='enter-event-token'),
    path('event-delete/', DeleteEventsAPI.as_view(), name='event-delete'),
    path('event-edit/', EditEventsAPI.as_view(), name='event-edit'),
    path('event-search/', Event_SearchAPI.as_view(), name='event-search'),
    path('session-delete/', DeleteSessionsAPI.as_view(), name='session-delete'),
    path('session-get/', GetSessionssAPI.as_view(), name='session-get'),
    path('session-get-day/', GetSessionsDayAPI.as_view(), name='session-get-day'),
    path('session-join/', JoinSessionssAPI.as_view(), name='session-join'),
    path('session-cancel/', CancelSessionssAPI.as_view(), name='session-cancel'),
]
