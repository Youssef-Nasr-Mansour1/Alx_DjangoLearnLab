from rest_framework.generics import ListAPIView
from .models import Book
from .serializers import BookSerializer
from rest_framework import generics
from rest_framework import viewsets


class BookList(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
  

class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()  # The data to be exposed via the API
    serializer_class = BookSerializer  # The serializer that converts model instances into JSON


from rest_framework.permissions import IsAuthenticated, IsAdminUser

class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]  # Only authenticated users can access
