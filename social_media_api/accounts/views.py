# accounts/views.py
from rest_framework import generics, status
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from .models import CustomUser
from .serializers import UserRegistrationSerializer, UserProfileSerializer

class UserRegistrationView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserRegistrationSerializer

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        token, created = Token.objects.get_or_create(user=response.data['id'])
        return Response({'token': token.key}, status=status.HTTP_201_CREATED)

class UserLoginView(APIView):
    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        if user:
            token, created = Token.objects.get_or_create(user=user)
            return Response({'token': token.key}, status=status.HTTP_200_OK)
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

class UserProfileView(generics.RetrieveUpdateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserProfileSerializer

    def get_object(self):
        return self.request.user
    
    from rest_framework import views, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import get_user_model

User = get_user_model()

class FollowUserView(views.APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, user_id):
        try:
            user_to_follow = User.objects.get(id=user_id)
            if user_to_follow == request.user:
                return Response({"detail": "You cannot follow yourself."}, status=status.HTTP_400_BAD_REQUEST)
            request.user.following.add(user_to_follow)
            return Response({"detail": f"Successfully followed {user_to_follow.username}"}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({"detail": "User not found."}, status=status.HTTP_404_NOT_FOUND)

class UnfollowUserView(views.APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, user_id):
        try:
            user_to_unfollow = User.objects.get(id=user_id)
            if user_to_unfollow == request.user:
                return Response({"detail": "You cannot unfollow yourself."}, status=status.HTTP_400_BAD_REQUEST)
            request.user.following.remove(user_to_unfollow)
            return Response({"detail": f"Successfully unfollowed {user_to_unfollow.username}"}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({"detail": "User not found."}, status=status.HTTP_404_NOT_FOUND)


