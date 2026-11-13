from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from .models import Category, Listing
from .validators import no_links
from django.utils import timezone
from datetime import timedelta


class CategorySerializer(serializers.ModelSerializer):
    active_listings = serializers.IntegerField(read_only=True)
    class Meta:
        model = Category
        fields = ["id", "name", "slug", "active_listings"]
        extra_kwargs = {
            "name": {"validators": [UniqueValidator(queryset=Category.objects.all(), lookup="iexact")]},
            "slug": {"help_text": "Латиница, цифры и дефисы",
                     "validators": [UniqueValidator(queryset=Category.objects.all(), lookup="iexact")]}

        }

    def validate_slug(self, slug):
        return slug.lower()

class ListingSerializer(serializers.ModelSerializer):
    seller = serializers.SlugRelatedField(slug_field="username", read_only=True)
    category = CategorySerializer(read_only=True)

    class Meta:
        model = Listing
        fields = [
            "id", "title", "description", "price", "category",
            "city", "status", "seller", "created_at", "updated_at",
        ]

class ListingCardSerializer(serializers.ModelSerializer):
    is_mine = serializers.SerializerMethodField()
    is_new = serializers.SerializerMethodField()
    category_name = serializers.CharField(source='category.name', read_only=True)
    seller_name = serializers.CharField(source='seller.username', read_only=True)

    class Meta:
        model = Listing
        fields = ['id', 'title', 'price', 'city', 'status',
                  'category_name', 'seller_name', 'is_new', 'is_mine']

    def get_is_new(self, obj):
        return obj.created_at >= timezone.now() - timedelta(days=3)

    def get_is_mine(self, obj):
        request = self.context.get("request")
        return bool(request) and obj.seller_id == request.user.id


class ListingWriteSerializer(serializers.ModelSerializer):

    seller = serializers.HiddenField(default=serializers.CurrentUserDefault())
    class Meta:
        model = Listing
        fields = [
            'title', 'description', 'price', 'category', 'city', 'status', 'seller'
        ]

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













