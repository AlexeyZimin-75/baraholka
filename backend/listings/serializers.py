from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from .models import Category, Listing


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name", "slug"]
        extra_kwargs = {
            "name": {"validators": [UniqueValidator(queryset=Category.objects.all(), lookup="iexact")]},
            "slug": {"help_text": "Латиница, цифры и дефисы",
                     "validators": [UniqueValidator(queryset=Category.objects.all(), lookup="iexact")]}

        }

"""
    title = models.CharField(max_length=120)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.PROTECT,  related_name="listings")
    seller = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="listings")
    city = models.CharField(max_length=100)
    status = models.CharField(max_length=30, choices=Status.choices, default=Status.ACTIVE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
"""

class ListingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Listing
        fields = [
            "id", "title", "description", "price", "category",
                "city", "status", "seller", "created_at", "updated_at"]

        read_only_fields = ["seller", "created_at", "updated_at"]