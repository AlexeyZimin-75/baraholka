from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    email = models.EmailField("email", unique=True)
    city = models.CharField(max_length=100, blank=True)

    def __str__(self) -> str:
        return self.username
