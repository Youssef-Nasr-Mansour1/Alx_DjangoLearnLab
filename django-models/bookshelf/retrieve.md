# Retrieve Book Attributes

To retrieve a specific book using Django's ORM, use the following command:

```python
book = Book.objects.get(title="1984")
