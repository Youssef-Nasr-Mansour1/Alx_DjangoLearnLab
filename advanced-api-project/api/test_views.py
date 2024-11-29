from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.contrib.auth.models import User
from .models import Book

class BookAPITests(APITestCase):
    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(username="testuser", password="password123")
        self.client = APIClient()
        self.client.login(username="testuser", password="password123")
        
        # Create sample books
        self.book1 = Book.objects.create(title="Book One", author="Author One", price=10.99)
        self.book2 = Book.objects.create(title="Book Two", author="Author Two", price=12.99)

    def test_create_book(self):
        # Test creating a new book
        data = {"title": "Book Three", "author": "Author Three", "price": 15.99}
        response = self.client.post("/api/books/", data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.count(), 3)

    def test_retrieve_book(self):
        # Test retrieving a book
        response = self.client.get(f"/api/books/{self.book1.id}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], "Book One")

    def test_update_book(self):
        # Test updating a book
        data = {"title": "Updated Book One"}
        response = self.client.patch(f"/api/books/{self.book1.id}/", data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.book1.refresh_from_db()
        self.assertEqual(self.book1.title, "Updated Book One")

    def test_delete_book(self):
        # Test deleting a book
        response = self.client.delete(f"/api/books/{self.book1.id}/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Book.objects.count(), 1)

    def test_filter_books(self):
        # Test filtering books by author
        response = self.client.get("/api/books/?author=Author One")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["author"], "Author One")

    def test_search_books(self):
        # Test searching for books
        response = self.client.get("/api/books/?search=Book")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_order_books(self):
        # Test ordering books by price
        response = self.client.get("/api/books/?ordering=price")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        prices = [book["price"] for book in response.data]
        self.assertEqual(prices, sorted(prices))
