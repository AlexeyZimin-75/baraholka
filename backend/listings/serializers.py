from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from .models import Category, Listing
from .validators import no_links


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name", "slug"]
        extra_kwargs = {
            "name": {"validators": [UniqueValidator(queryset=Category.objects.all(), lookup="iexact")]},
            "slug": {"help_text": "Латиница, цифры и дефисы",
                     "validators": [UniqueValidator(queryset=Category.objects.all(), lookup="iexact")]}

        }

    def validate_slug(self, slug):
        return slug.lower()

class ListingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Listing
        fields = [
            "id", "title", "description", "price", "category",
                "city", "status", "seller", "created_at", "updated_at"]

        read_only_fields = ["seller", "created_at", "updated_at"]

        extra_kwargs = {
            "title": {"validators": [no_links]},
            "description": {"validators": [no_links]}
        }

    def validate_price(self, price):
        if price <= 0:
            raise serializers.ValidationError("Цена должна быть больше нуля!")
        return price

    def validate(self, attrs):
        status = attrs.get("status", getattr(self.instance, "status", Listing.Status.ACTIVE))
        description = attrs.get("description", getattr(self.instance, "description", ""))
        if status == Listing.Status.ACTIVE and len(description.strip()) < 20:
            raise serializers.ValidationError({'description': 'Если объявление активно, описание должно быть не меньше 20 символов'})
        return attrs





