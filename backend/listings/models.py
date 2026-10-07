from django.db import models
from django.conf import settings

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True)

    class Meta:
        ordering = ['name']

    def __str__(self) -> str:
        return self.name

class Listing(models.Model):
    class Status(models.TextChoices):
        DRAFT = "draft", "в черновиках"
        ACTIVE = "active", "активное"
        SOLD = "sold", "распродано"
        ARCHIVED = "archived", "в архиве"


    title = models.CharField(max_length=120)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.PROTECT,  related_name="listings")
    seller = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="listings")
    city = models.CharField(max_length=100)
    status = models.CharField(max_length=30, choices=Status.choices, default=Status.ACTIVE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self) -> str:
        return self.title




