from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    USER_ROLE_CHOICES = [
        ('Admin', 'Admin'),
        ('Librarian', 'Librarian'),
        ('Member', 'Member'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=USER_ROLE_CHOICES, default='Member')

    def __str__(self):
        return f'{self.user.username} - {self.role}'
