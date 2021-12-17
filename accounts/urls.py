from .views import RegisterAPI, LoginAPI, ChangePasswordView, EditAPI, CurrentUserAPI
from django.urls import path, include
from knox import views as knox_views
from django.conf import settings
from django.conf.urls.static import static




urlpatterns = [
    
    path('register/', RegisterAPI.as_view(), name='register'),
    path('login/', LoginAPI.as_view(), name='login'),
    path('edit-profile/', EditAPI.as_view(), name='edit-profile'),
    path('user/', CurrentUserAPI.as_view()),
    path('logout/', knox_views.LogoutView.as_view(), name='logout'),
    path('change-password/', ChangePasswordView.as_view(), name='change-password'),
    path('password-reset/', include('django_rest_passwordreset.urls', namespace='password-reset')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)