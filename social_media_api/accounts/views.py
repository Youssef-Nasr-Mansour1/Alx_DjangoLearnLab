from rest_framework import generics, status, permissions
from rest_framework.response import Response
from django.contrib.auth import get_user_model

# Fetch the CustomUser model
CustomUser = get_user_model()

class FollowUserView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]  # Ensures only authenticated users can follow/unfollow

    def post(self, request, user_id, *args, **kwargs):
        try:
            user_to_follow = CustomUser.objects.get(id=user_id)  # Query CustomUser instead of User
            if user_to_follow == request.user:
                return Response({"detail": "You cannot follow yourself."}, status=status.HTTP_400_BAD_REQUEST)
            request.user.following.add(user_to_follow)
            return Response({"detail": f"Successfully followed {user_to_follow.username}"}, status=status.HTTP_200_OK)
        except CustomUser.DoesNotExist:
            return Response({"detail": "User not found."}, status=status.HTTP_404_NOT_FOUND)

class UnfollowUserView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]  # Ensures only authenticated users can follow/unfollow

    def post(self, request, user_id, *args, **kwargs):
        try:
            user_to_unfollow = CustomUser.objects.get(id=user_id)  # Query CustomUser instead of User
            if user_to_unfollow == request.user:
                return Response({"detail": "You cannot unfollow yourself."}, status=status.HTTP_400_BAD_REQUEST)
            request.user.following.remove(user_to_unfollow)
            return Response({"detail": f"Successfully unfollowed {user_to_unfollow.username}"}, status=status.HTTP_200_OK)
        except CustomUser.DoesNotExist:
            return Response({"detail": "User not found."}, status=status.HTTP_404_NOT_FOUND)
