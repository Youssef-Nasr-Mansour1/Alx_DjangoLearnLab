from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PostViewSet, CommentViewSet, FeedViewSet

# Initialize the router
router = DefaultRouter()

# Register viewsets with the router
router.register(r'posts', PostViewSet, basename='post')
router.register(r'comments', CommentViewSet, basename='comment')
router.register(r'feed', FeedViewSet, basename='feed')

# Define the URL patterns
urlpatterns = [
    path('', include(router.urls)),
]
