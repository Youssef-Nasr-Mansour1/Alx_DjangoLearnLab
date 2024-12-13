# views.py
from rest_framework import viewsets, permissions, filters, status, generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from .models import Post, Comment, Like
from .serializers import PostSerializer, CommentSerializer
from notifications.models import Notification

# User model reference
User = get_user_model()

# Abstract ViewSet to handle common functionality for Post and Comment ViewSets
class AuthorMixin:
    """Mixin to automatically set the author of the post or comment."""
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class PostViewSet(AuthorMixin, viewsets.ModelViewSet):
    """
    ViewSet for managing Posts.
    Includes functionality for authenticated users to create posts and for everyone to read posts.
    """
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [filters.SearchFilter]
    search_fields = ['title', 'content']

    def get_queryset(self):
        """
        Optionally restricts the returned posts to the user's feed (following users).
        """
        user = self.request.user
        following_users = user.following.all()
        queryset = Post.objects.filter(author__in=following_users).order_by('-created_at') if following_users.exists() else Post.objects.all().order_by('-created_at')
        return queryset


class CommentViewSet(AuthorMixin, viewsets.ModelViewSet):
    """
    ViewSet for managing Comments.
    Includes functionality for authenticated users to create comments and for everyone to read comments.
    """
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        """
        Filter comments by post ID.
        """
        post_id = self.request.query_params.get('post', None)
        if post_id is not None:
            return Comment.objects.filter(post_id=post_id).order_by('-created_at')
        return Comment.objects.all().order_by('-created_at')


class FeedViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for the feed of posts from followed users.
    Only accessible by authenticated users.
    """
    permission_classes = [IsAuthenticated]
    serializer_class = PostSerializer

    def get_queryset(self):
        """Filter the posts based on the users the current user is following."""
        user = self.request.user
        following_users = user.following.all()
        return Post.objects.filter(author__in=following_users).order_by('-created_at')


# Like Post and Unlike Post Views
class LikePostView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        user = request.user
        post = Post.objects.filter(id=pk).first()
        
        if not post:
            return Response({"detail": "Post not found."}, status=status.HTTP_404_NOT_FOUND)

        # Check if user has already liked the post
        if Like.objects.filter(user=user, post=post).exists():
            return Response({"detail": "You have already liked this post."}, status=status.HTTP_400_BAD_REQUEST)

        # Like the post
        Like.objects.create(user=user, post=post)

        # Create a notification
        notification = Notification.objects.create(
            recipient=post.author,
            actor=user,
            verb="liked your post",
            target_ct=ContentType.objects.get_for_model(post),
            target_id=post.id
        )

        return Response({"detail": "Post liked!"}, status=status.HTTP_200_OK)


class UnlikePostView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        user = request.user
        post = Post.objects.filter(id=pk).first()

        if not post:
            return Response({"detail": "Post not found."}, status=status.HTTP_404_NOT_FOUND)

        # Check if user has liked the post
        like = Like.objects.filter(user=user, post=post).first()
        if not like:
            return Response({"detail": "You have not liked this post."}, status=status.HTTP_400_BAD_REQUEST)

        # Unlike the post
        like.delete()

        # Optionally, create a notification for unliking if needed
        # For now, we do not create a notification for unliking posts, but this could be implemented if desired.

        return Response({"detail": "Post unliked!"}, status=status.HTTP_200_OK)

