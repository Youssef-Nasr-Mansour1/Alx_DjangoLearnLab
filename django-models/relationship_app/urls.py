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
    path('login/', LoginView.as_view(template_name='relationship_app/login.html'), name='login'),
    path('logout/', LogoutView.as_view(template_name='relationship_app/logout.html'), name='logout'),
    path('register/', views.register, name='register'),  # Keep the register view as function-based
]

# relationship_app/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('admin/', views.admin_view, name='admin_view'),
    path('librarian/', views.librarian_view, name='librarian_view'),
    path('member/', views.member_view, name='member_view'),
]
