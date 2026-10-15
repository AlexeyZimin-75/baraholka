from django.urls import path

from .views import  CategoryDetail, CategoryList


urlpatterns = [
    path('categories/', CategoryList.as_view(), name="category-list"),
    path('categories/<int:id>/', CategoryDetail.as_view(), name="category-detail")
]