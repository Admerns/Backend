from django.urls import path, include
from .views import GoogleCalendarLoginAPI

urlpatterns = [
    path('login_create/', GoogleCalendarLoginAPI.as_view(), name='googlecalendar_login-create'),
]
