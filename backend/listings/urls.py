from django.urls import path

from .views import  CategoryDetail, CategoryList, CategoryListings, ListingCreate, ListingDetail


urlpatterns = [
    path('categories/', CategoryList.as_view(), name="category-list"),
    path('categories/<int:id>/', CategoryDetail.as_view(), name="category-detail"),
    path('listings/', ListingCreate.as_view(), name='listing-create'),
    path('categories/<int:id>/listings/', CategoryListings.as_view(), name='listings'),
    path('listings/<int:id>/', ListingDetail.as_view(), name="listing-detail")


]