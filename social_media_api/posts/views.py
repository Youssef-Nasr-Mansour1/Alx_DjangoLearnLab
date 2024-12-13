from rest_framework import status, generics
from rest_framework.permissions.IsAuthenticated import IsAuthenticated  # Import IsAuthenticated permission
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Post, Like
from .serializers import PostSerializer
from notifications.models import Notification
from django.contrib.contenttypes.models import ContentType

class LikePostView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]  # Ensures that only authenticated users can like a post

    def post(self, request, pk):
        user = request.user
        post = get_object_or_404(Post, pk=pk)  # Get the post or return a 404 if not found

        # Get or create the like instance (prevents liking the post multiple times by the same user)
        like, created = Like.objects.get_or_create(user=request.user, post=post)

        if not created:  # If the like already exists, return a 400 error
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
    permission_classes = [IsAuthenticated]  # Ensures that only authenticated users can unlike a post

    def post(self, request, pk):
        user = request.user
        post = generics.get_object_or_404(Post, pk=pk)  # Get the post or return a 404 if not found

        # Check if the user has already liked the post
        like = Like.objects.filter(user=user, post=post).first()

        if not like:  # If no like exists, return a 400 error
            return Response({"detail": "You have not liked this post."}, status=status.HTTP_400_BAD_REQUEST)

        # Delete the like
        like.delete()

        return Response({"detail": "Post unliked!"}, status=status.HTTP_200_OK)
