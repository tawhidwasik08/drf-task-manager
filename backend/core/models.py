from django.db import models
from django.contrib.auth.models import AbstractUser

class UserProfile(AbstractUser):
    """
    Custom user profile model.

    Inherits from AbstractUser and extends it with additional fields.

    Fields:
        id (AutoField): The unique identifier for the user.
        username (CharField): The username of the user.
        password (CharField): The password of the user.
        role (CharField): The role of the user.
        email (EmailField): The email address of the user.
    """
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('manager', 'Manager'),
        ('team_member', 'Team Member'),
    ]

    class Meta:
        verbose_name_plural = "Users"

    role = models.CharField(max_length=50, null=False, choices=ROLE_CHOICES, verbose_name="User role")
    email = models.EmailField(unique=True)

    def __str__(self):
        return f'{self.username} ({self.role})'
