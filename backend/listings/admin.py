from django.contrib import admin
from .models import Category, Listing

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["name", "slug"]
    prepopulated_fields = {"slug": ["name"]}


@admin.register(Listing)
class ListingAdmin(admin.ModelAdmin):
    list_display = ["title", "price",
                    "category", "seller", "city", "status", "created_at", "updated_at"]
    list_filter = ["status", "category"]
    search_fields = ["title", "description"]

