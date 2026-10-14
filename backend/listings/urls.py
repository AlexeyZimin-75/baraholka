from django.urls import path

from .views import category_list, category_detail


urlpatterns = [
    path('categories/', category_list, name="category-list"),
    path('categories/<int:id>/', category_detail, name="category-detail")
]