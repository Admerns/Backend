from .views import RegisterAPI, LoginAPI, ChangePasswordView, EditAPI
from django.urls import path, include
from knox import views as knox_views




urlpatterns = [
    
    path('register/', RegisterAPI.as_view(), name='register'),
    path('login/', LoginAPI.as_view(), name='login'),
    path('edit/', EditAPI.as_view(), name='edit'),
    path('logout/', knox_views.LogoutView.as_view(), name='logout'),
    path('change-password/', ChangePasswordView.as_view(), name='change-password'),
    path('password-reset/', include('django_rest_passwordreset.urls', namespace='password-reset')),
]