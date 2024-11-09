# relationship_app/urls.py
from django.urls import path
from . import views
from .views import list_books

urlpatterns = [
    path('books/', views.list_books, name='list_books'),  # Function-based view URL
    path('library/<int:pk>/', views.LibraryDetailView.as_view(), name='library_detail'),  # Class-based view URL
]

# relationship_app/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),  # Login URL
    path('logout/', views.logout_view, name='logout'),  # Logout URL
    path('register/', views.register, name='register'),  # Register URL
]
