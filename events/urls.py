from django.urls import path, include
from .views import DeleteSessionsAPI, EventsAPI, Event_SessionsAPI, GetEventsAPI, DeleteEventsAPI
from .views import EditEventsAPI, Event_SearchAPI, DeleteSessionsAPI, GetSessionssAPI

urlpatterns = [
    path('event-create/', EventsAPI.as_view(), name='event-create'),
    path('event-get/', GetEventsAPI.as_view(), name='event-get'),
    path('enter-event-token/', Event_SessionsAPI.as_view(), name='enter-event-token'),
    path('event-delete/', DeleteEventsAPI.as_view(), name='event-delete'),
    path('event-edit/', EditEventsAPI.as_view(), name='event-edit'),
    path('event-search/', Event_SearchAPI.as_view(), name='event-search'),
    path('session-delete/', DeleteSessionsAPI.as_view(), name='session-delete'),
    path('session-get/', GetSessionssAPI.as_view(), name='session-get'),
]