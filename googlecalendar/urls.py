from django.urls import path, include
from .views import GoogleCalendarLoginAPI

urlpatterns = [
    path('googlecalendar_login-create/', GoogleCalendarLoginAPI.as_view(), name='googlecalendar_login-create'),
]
