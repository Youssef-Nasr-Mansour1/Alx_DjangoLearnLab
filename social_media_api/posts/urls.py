from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PostViewSet, CommentViewSet, FeedViewSet

# Create a router to register views
router = DefaultRouter()
router.register(r'posts', PostViewSet, basename='post')
router.register(r'comments', CommentViewSet, basename='comment')
router.register(r'feed', FeedViewSet, basename='feed/')  # Add feed endpoint here

# Include the router URLs
urlpatterns = [
    path('', include(router.urls)),  # This includes all routes from the router
]
