from django.urls import path, include
from .views import GoogleCalendarLoginAPI, CoordinatesAPI, GetAppAPI

urlpatterns = [
    path('login_create/', GoogleCalendarLoginAPI.as_view(), name='googlecalendar_login-create'),
    path('coordinates/', CoordinatesAPI.as_view(), name='coordinates'),
    path('Android_Application/', GetAppAPI.as_view(), name='Get App')
]
