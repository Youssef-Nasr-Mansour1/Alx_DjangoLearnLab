# Delete Book

To delete the book you created and confirm the deletion by trying to retrieve all books again, use the following Python commands:

```python
from bookshelf.models import Book  # Import the Book model

# Assuming you have already retrieved the book instance and it's stored in the variable 'book'

# Delete the book
book.delete()

# Confirm the deletion by attempting to retrieve all books
all_books = Book.objects.all()
