# posts/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PostViewSet, CommentViewSet, FeedViewSet, LikePostView, UnlikePostView
from notifications.views import NotificationListView

# Create a router to register views
router = DefaultRouter()
router.register(r'posts', PostViewSet, basename='post')
router.register(r'comments', CommentViewSet, basename='comment')
router.register(r'feed', FeedViewSet, basename='feed/')  # Corrected basename

# Define URL patterns for likes, unlikes, and notifications
urlpatterns = [
    path('', include(router.urls)),  # Includes all routes from the router
    path('posts/<int:pk>/like/', LikePostView.as_view(), name='like-post'),
    path('posts/<int:pk>/unlike/', UnlikePostView.as_view(), name='unlike-post'),
    path('notifications/', NotificationListView.as_view(), name='notifications'),
]
