from django.urls import path, include
from .views import EventsAPI, Event_SessionsAPI, GetEventsAPI, DeleteEventsAPI, EditEventsAPI, Event_SearchAPI

urlpatterns = [
    path('event-create/', EventsAPI.as_view(), name='event-create'),
    path('event-get/', GetEventsAPI.as_view(), name='event-get'),
    path('enter-event-token/', Event_SessionsAPI.as_view(), name='enter-event-token'),
    path('event-delete/', DeleteEventsAPI.as_view(), name='event-delete'),
    path('event-edit/', EditEventsAPI.as_view(), name='event-edit'),
    path('event-search/', Event_SearchAPI.as_view(), name='event-search'),
]