from django.contrib.auth.models import User
from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated 
from rest_framework.response import Response
from rest_framework import generics, status
from .serializers import GoogleCalendarLogin_CreateSerializer, Coordinates_CreateSerializer
from accounts.models import Metadata
from geopy.geocoders import Nominatim

# Create your views here.

class GoogleCalendarLoginAPI(generics.GenericAPIView):
    serializer_class = GoogleCalendarLogin_CreateSerializer
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        userid = request.user.id
        request.data['userid'] = userid
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class CoordinatesAPI(generics.GenericAPIView):
    serializer_class = Coordinates_CreateSerializer
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):

        user = request.user
        try :
            metadata = user.metadata
  
        except Exception as e:
            metadata = Metadata(user=user)


        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            geolocator = Nominatim(user_agent="geoapiExercises")
            Latitude = request.data['latitude']
            Longitude = request.data['longitude']
            location = geolocator.reverse(Latitude+","+Longitude, language='en')
            
            try:
                city = str(location.raw['address']['state'])
                metadata.city = city
            except:
                city = str(location.raw['address']['province'])
                metadata.city = city

            if ("Province" in metadata.city):
                metadata.city = metadata.city.replace(" Province", "")
     
            metadata.save()
            response = {
                        'status': 'success',
                        'code': status.HTTP_200_OK,
                        'message': 'City added successfuly.',
                        'data': []
                    }
            return Response(response)
        except:
            response = {
                'message': 'Coordinates error.',
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
        