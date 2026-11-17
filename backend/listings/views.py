from typing import Any

from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status
from .models import Category, Listing
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.exceptions import ValidationError, PermissionDenied, APIException
from .serializers import CategorySerializer, ListingCardSerializer, ListingWriteSerializer, ListingSerializer
from django.db.models import Count, Q
from rest_framework.permissions import IsAuthenticated
from rest_framework import permissions, generics
from rest_framework.mixins import *

class CategoryNotEmpty(APIException):
    status_code = 409
    default_detail = "Нельзя удалять категорию, в которой есть объявления"


class IsSeller(permissions.BasePermission):
    message = "Можно менять только свои объявления."
    def has_object_permission(self, request: Request, view: APIView, obj: Any) -> bool:


        if request.method in permissions.SAFE_METHODS:
            return True

        if request.user.id == obj.seller_id:
            return True

        raise PermissionDenied(detail=self.message)

def categories_with_counts():
    return Category.objects.annotate(
        active_listings = Count("listings", filter=Q(listings__status=Listing.Status.ACTIVE))
    )


class CategoryDetail(RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin, generics.GenericAPIView):
    serializer_class = CategorySerializer
    queryset = categories_with_counts()
    lookup_url_kwarg = "id"

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

    def perform_destroy(self, instance) -> None:
        if instance.listings.exists():
            raise CategoryNotEmpty
        instance.delete()


class CategoryList(ListModelMixin, CreateModelMixin, generics.GenericAPIView):
    serializer_class = CategorySerializer
    queryset = categories_with_counts()

    def get_queryset(self):
        categories = super().get_queryset()
        search = self.request.query_params.get("search", "").strip()
        if search:
            categories = categories.filter(name__icontains=search)
        return categories

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class CategoryListings(generics.GenericAPIView):
    queryset = Listing.objects.select_related("seller", "category")
    serializer_class = ListingCardSerializer

    def get_queryset(self):
        category = get_object_or_404(Category, id=self.kwargs['id'])
        listings = super().get_queryset().filter(category=category)
        listing_status = self.request.query_params.get("status", "").strip()
        if listing_status in Listing.Status.values:
            listings = listings.filter(status=listing_status)
        elif listing_status and listing_status not in Listing.Status.values:
            raise ValidationError({"status": ["неизвестный статус объявления"]})
        return listings

    def get(self, request, id):
        serializer = self.get_serializer(self.get_queryset(), many=True)
        return Response(serializer.data)

class ListingCreate(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = ListingWriteSerializer(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        listing = serializer.save()
        return Response(ListingSerializer(listing).data, status=status.HTTP_201_CREATED)

class ListingDetail(generics.GenericAPIView):
    permission_classes = [IsSeller]
    queryset = Listing.objects.select_related("seller", "category")
    serializer_class = ListingSerializer
    lookup_url_kwarg = "id"

    def get(self, request, id):
        return Response(self.get_serializer(self.get_object()).data)

    def patch(self, request, id):
        serializer = ListingWriteSerializer(self.get_object(), data=request.data, context=self.get_serializer_context(),
                                            partial=True)
        serializer.is_valid(raise_exception=True)
        new_data = serializer.save()
        return Response(self.get_serializer(new_data).data)







