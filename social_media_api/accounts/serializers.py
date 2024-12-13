from rest_framework import serializers
from rest_framework.authtoken.models import Token
from django.contrib.auth import get_user_model

# Get the user model dynamically to support custom user models
User = get_user_model()

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)  # Password should only be writable

    class Meta:
        model = User
        fields = ['username', 'email', 'password']  # Fields exposed via the API

    def create(self, validated_data):
        # Create the user using the custom user model's create_user method
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        # Generate an authentication token for the new user
        Token.objects.create(user=user)
        return user

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)
