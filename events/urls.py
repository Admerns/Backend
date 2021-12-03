from django.urls import path, include


from .views import Event_SessionsAPI, EventsAPI, GetEventsAPI

urlpatterns = [
    path('event-create/', EventsAPI.as_view(), name='event-create'),
    path('event-get/', GetEventsAPI.as_view(), name='event-get'),
    path('event-sessions/', Event_SessionsAPI.as_view(), name='event-sessions'),
]