from django.urls import path, include
from .views import EventsAPI, EnterEventAPI, GetEventsAPI

urlpatterns = [
    path('event-create/', EventsAPI.as_view(), name='event-create'),
    path('event-get/', GetEventsAPI.as_view(), name='event-get'),
    path('enter-event-token/', EnterEventAPI.as_view(), name='enter-event-token'),
]