from rest_framework import generics, permissions, status
from rest_framework.response import Response
from knox.models import AuthToken

from accounts.models import UserProfile

from .serializers import GetUserSerializer, UserSerializer,LoginSerializer, RegisterSerializer, ChangePasswordSerializer, EditSerializer

from django.contrib.auth import login
from rest_framework.authtoken.serializers import AuthTokenSerializer
from knox.views import LoginView as KnoxLoginView
from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated 

# Return Current User API
class CurrentUserAPI(generics.GenericAPIView):
    serializer_class = UserSerializer
    def post(self, request):
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)

class GetProfileAPI(generics.GenericAPIView):
    serializer_class = GetUserSerializer
    def post(self, request, *args, **kwargs):
        try:
            user = User.objects.filter(username = request.data['username']).first()
            serializer = self.get_serializer(user)
            return Response(serializer.data)
        except Exception as e:
            response = {
                'message': 'User not found.',
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)



# Register API
class RegisterAPI(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        profile = UserProfile(user=user)
        profile.save()
        return Response({
        "user": UserSerializer(user, context=self.get_serializer_context()).data
        })

class LoginAPI(KnoxLoginView, generics.GenericAPIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = LoginSerializer
    def post(self, request):
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        return super(LoginAPI, self).post(request, format=None)


class ChangePasswordView(generics.UpdateAPIView):
    """
    An endpoint for changing password.
    """
    serializer_class = ChangePasswordSerializer
    model = User
    permission_classes = (IsAuthenticated,)

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data, files=request.FILES)

        if serializer.is_valid():
            # Check old password
            if not self.object.check_password(serializer.data.get("old_password")):
                return Response({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)
            # set_password also hashes the password that the user will get
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            response = {
                'status': 'success',
                'code': status.HTTP_200_OK,
                'message': 'Password updated successfully',
                'data': []
            }

            return Response(response)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class EditAPI(generics.UpdateAPIView):
    serializer_class = EditSerializer
    model = User
    permission_classes = (IsAuthenticated,)

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            if(serializer.data.get("email") != None and serializer.data.get("email") != ""):
                self.object.email = (serializer.data.get("email"))
            if(serializer.data.get("first_name") != None):
                self.object.first_name = (serializer.data.get("first_name"))
            if(serializer.data.get("last_name") != None ):
                self.object.last_name = (serializer.data.get("last_name"))
            self.object.save()

            profile = self.object.userprofile

            if(serializer.data.get("phone_number") != None ):
                profile.phone_number = (serializer.data.get("phone_number"))
            try:
                if(serializer.validated_data["avatar"] != None ):
                    profile.avatar = ((serializer.validated_data["avatar"]))
            except Exception as e:
                pass

            profile.save()
            
            self.object.save()


            response = {
                'status': 'success',
                'code': status.HTTP_200_OK,
                'message': 'Profile updated successfully',
                'data': []
            }

            return Response(response)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
