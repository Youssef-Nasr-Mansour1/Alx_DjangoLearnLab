from django.urls import path
from .views import BookList
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('books/', BookList.as_view(), name='book-list'),
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),  # Include the API URLs
]

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BookViewSet

# Initialize the router
router = DefaultRouter()

# Register the BookViewSet with the router
router.register(r'books_all', BookViewSet, basename='book_all')

urlpatterns = [
    # Include the router URLs for all CRUD operations
    path('', include(router.urls)),
]
