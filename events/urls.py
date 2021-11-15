from django.urls import path, include
from .views import EventsAPI

urlpatterns = [
    path('event-create/', EventsAPI.as_view(), name='event-create'),
]