from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# UserProfile Model with predefined roles
class UserProfile(models.Model):
    # Define the available roles as constants for maintainability
    ADMIN = 'Admin'
    MEMBER = 'Member'
    
    ROLE_CHOICES = [
        (ADMIN, 'Admin'),
        (MEMBER, 'Member'),
    ]
    
    # Link UserProfile to the User model with a one-to-one relationship
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default=MEMBER)

    def __str__(self):
        # Display the username and the role in a readable format
        return f"{self.user.username} - {self.get_role_display()}"

# Signal to automatically create and save UserProfile when a User is created
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        # Create a UserProfile instance when a new User is created
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    # Save the UserProfile instance whenever the associated User instance is saved
    instance.userprofile.save()
