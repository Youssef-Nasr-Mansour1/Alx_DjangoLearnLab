from django.db import models

class Author(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Book(models.Model):
    title = models.CharField(max_length=200)
    publication_year = models.IntegerField()
    author = models.ForeignKey(Author, related_name="books", on_delete=models.CASCADE)

    def __str__(self):
        return self.title

# Author model: Represents authors in the system.
# Fields:
# - name: Name of the author (string).

# Book model: Represents books in the system.
# Fields:
# - title: Title of the book (string).
# - publication_year: Year the book was published (integer).
# - author: ForeignKey linking to the Author model.
