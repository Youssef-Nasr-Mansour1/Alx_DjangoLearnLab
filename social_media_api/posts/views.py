from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from .models import Post, Like
from .serializers import PostSerializer
from notifications.models import Notification
from django.contrib.contenttypes.models import ContentType

class LikePostView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]  # Ensuring the user is authenticated

    def post(self, request, pk):
        user = request.user
        # Safely retrieve the post or return 404 if not found
        post = get_object_or_404(Post, pk=pk)

        # Get or create the like instance, ensuring a user can only like a post once
        like, created = Like.objects.get_or_create(user=user, post=post)

        if not created:
            return Response({"detail": "You have already liked this post."}, status=status.HTTP_400_BAD_REQUEST)

        # Create a notification for the post's author
        notification = Notification.objects.create(
            recipient=post.author,
            actor=user,
            verb="liked your post",
            target_ct=ContentType.objects.get_for_model(post),
            target_id=post.id
        )

        return Response({"detail": "Post liked!"}, status=status.HTTP_200_OK)

class UnlikePostView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]  # Ensuring the user is authenticated

    def post(self, request, pk):
        user = request.user
        # Safely retrieve the post or return 404 if not found
        post = get_object_or_404(Post, pk=pk)

        # Check if the user has already liked the post
        like = Like.objects.filter(user=user, post=post).first()

        if not like:
            return Response({"detail": "You have not liked this post."}, status=status.HTTP_400_BAD_REQUEST)

        # Delete the like
        like.delete()

        return Response({"detail": "Post unliked!"}, status=status.HTTP_200_OK)
