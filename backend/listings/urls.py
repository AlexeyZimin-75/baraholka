from django.urls import path

from .views import  CategoryDetail, CategoryList, CategoryListings


urlpatterns = [
    path('categories/', CategoryList.as_view(), name="category-list"),
    path('categories/<int:id>/', CategoryDetail.as_view(), name="category-detail"),
    path('categories/<int:id>/listings/', CategoryListings.as_view(), name='listings')
]