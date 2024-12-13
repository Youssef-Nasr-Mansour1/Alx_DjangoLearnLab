from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Post, Like, Comment
from .serializers import PostSerializer, LikeSerializer, CommentSerializer
from notifications.models import Notification
from django.contrib.contenttypes.models import ContentType

class PostViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing posts.
    """
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]  # Only authenticated users can view/edit posts

class LikePostViewSet(viewsets.ViewSet):
    """
    A viewset for liking/unliking posts.
    """
    permission_classes = [IsAuthenticated]

    def like_post(self, request, pk=None):
        """
        Like a post.
        """
        user = request.user
        post = get_object_or_404(Post, pk=pk)

        # Get or create the like instance (prevents multiple likes by the same user)
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

    def unlike_post(self, request, pk=None):
        """
        Unlike a post.
        """
        user = request.user
        post = get_object_or_404(Post, pk=pk)

        # Check if the user has already liked the post
        like = Like.objects.filter(user=user, post=post).first()

        if not like:
            return Response({"detail": "You have not liked this post."}, status=status.HTTP_400_BAD_REQUEST)

        # Delete the like
        like.delete()

        return Response({"detail": "Post unliked!"}, status=status.HTTP_200_OK)

class CommentViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing comments on posts.
    """
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]  # Only authenticated users can comment

    def perform_create(self, serializer):
        """
        Overriding perform_create to associate comment with the logged-in user.
        """
        serializer.save(user=self.request.user)

# URLs configuration
from django.urls import path, include
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'posts', PostViewSet)
router.register(r'likes', LikePostViewSet, basename='like')  # Specify basename for Like viewset
router.register(r'comments', CommentViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
]
