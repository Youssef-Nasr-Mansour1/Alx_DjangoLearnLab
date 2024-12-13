from rest_framework import serializers
from django.contrib.auth import get_user_model

# Dynamically fetch the User model
User = get_user_model()

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField()  # Ensures password is write-only

    class Meta:
        model = User
        fields = ['username', 'email', 'password']  # Fields exposed in the API

    def create(self, validated_data):
        # Create a new user using the create_user method
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user
