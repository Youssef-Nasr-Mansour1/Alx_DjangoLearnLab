from django.contrib import admin
from django.urls import path, include
from .views import FollowUserView, UnfollowUserView

# App name for namespacing the URLs
app_name = 'social_media_api'

urlpatterns = [
    # Admin panel URL
    path('admin/', admin.site.urls),
    
    # Include URLs from 'posts' app for handling post-related views
    path('api/', include('posts.urls')),
    
    # Follow/unfollow user endpoints
    path('follow/<int:user_id>/', FollowUserView.as_view(), name='follow-user'),
    path('unfollow/<int:user_id>/', UnfollowUserView.as_view(), name='unfollow-user'),
]
