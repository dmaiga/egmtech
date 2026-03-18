#accounts/models
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):

    ROLE_CHOICES = (
        ("CLIENT", "Client"),
        ("ADMIN", "Admin"),
    )

    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20, unique=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default="CLIENT")
    
    avatar = models.ImageField(upload_to="avatars/", null=True, blank=True)
    
    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email", "phone"]

    def __str__(self):
        return self.username