from django.urls import path, include
from .views import GoogleCalendarLoginAPI, CoordinatesAPI

urlpatterns = [
    path('login_create/', GoogleCalendarLoginAPI.as_view(), name='googlecalendar_login-create'),
    path('coordinates/', CoordinatesAPI.as_view(), name='coordinates'),
]
