from rest_framework import serializers
from django.contrib.auth.models import User
from django.forms import ValidationError
from rest_framework.fields import CharField
import re

# User Serializer
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email')

# Register Serializer
class RegisterSerializer(serializers.ModelSerializer):

    password2 = CharField(label='Confirm Password')

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password', 'password2','first_name', 'last_name')
        extra_kwargs = {'password': {'write_only': True},'password2': {'write_only': True},'first_name': {'required': True},'last_name': {'required': True}}

    def validate(self, data):
        password = data.get('password')
        confirm_password = data.pop('password2')
        if password != confirm_password:
            raise ValidationError('Passwords dont match!')
        elif len(password) < 8:
            raise ValidationError("Make sure your password is at lest 8 letters")
        elif re.search('[0-9]',password) is None:
            raise ValidationError("Make sure your password has a number in it")
        elif re.search('[A-Z]',password) is None: 
            raise ValidationError("Make sure your password has a capital letter in it")
        return data


    def create (self, validated_data):
        email = validated_data.get('email')
        username = validated_data.get('username')
        password = validated_data.get('password')
        
        try:
            user = User.objects.create(username=username, email=email)
            user.set_password(password)
            user.first_name = validated_data['first_name']
            user.last_name  = validated_data['last_name']
            user.save()
            return user
        except Exception as e:
            return e

class ChangePasswordSerializer(serializers.Serializer):
    model = User

    def validate(self, data):
        password = data.get('new_password')
        if len(password) < 8:
            raise ValidationError("Make sure your password is at lest 8 letters")
        elif re.search('[0-9]',password) is None:
            raise ValidationError("Make sure your password has a number in it")
        elif re.search('[A-Z]',password) is None: 
            raise ValidationError("Make sure your password has a capital letter in it")
        return data

    """
    Serializer for password change endpoint.
    """
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)


# Login Serializer
class LoginSerializer(serializers.ModelSerializer):

    password = serializers.CharField(
        write_only=True,
        required=True,
        help_text='Enter your password',
        style={'input_type': 'password', 'placeholder': 'Password'}
    )

    class Meta:
        model = User
        fields = ('username', 'password')