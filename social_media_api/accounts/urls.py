from django.urls import path
from .views import UserRegistrationView, UserLoginView, UserProfileView

app_name = 'accounts'  # Added app_name for namespacing the URLs

urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('profile/', UserProfileView.as_view(), name='profile'),
]

