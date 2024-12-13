from rest_framework import viewsets, permissions, filters
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import get_user_model
from .models import Post, Comment
from .serializers import PostSerializer, CommentSerializer

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
        queryset = Post.objects.all()
        user = self.request.user
        following_users = user.following.all()
        if following_users.exists():
            queryset = queryset.filter(author__in=following_users).order_by('-created_at')
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

# Feed ViewSet - Shows posts from users the current user is following
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
