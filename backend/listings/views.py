from rest_framework.response import Response
from rest_framework import status
from .models import Category, Listing
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.exceptions import ValidationError
from .serializers import CategorySerializer, ListingSerializer

class CategoryDetail(APIView):
    def get_object(self, id):
        return get_object_or_404(Category, id=id)


    def get(self, request, id):
        return Response(CategorySerializer(self.get_object(id)).data)

    def patch(self, request, id):
        return self.update(request, id, partial=True)

    def put(self, request, id):
        return self.update(request, id, partial=False)

    def update(self, request, id, partial):
        serializer = CategorySerializer(self.get_object(id), data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def delete(self, request, id):
        category = self.get_object(id)
        if category.listings.exists():
            return Response({"detail": "В категории есть объявления"}, status=status.HTTP_409_CONFLICT)
        category.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)



class CategoryList(APIView):
    def get_queryset(self):
        categories = Category.objects.all()
        search = self.request.query_params.get("search", "").strip()
        if search:
            categories = categories.filter(name__icontains=search)
        return categories


    def get(self, request):
        serializer = CategorySerializer(self.get_queryset(), many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = CategorySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)





class CategoryListings(APIView):
    def get_queryset(self):
        category = get_object_or_404(Category, id=self.kwargs['id'])
        listings = Listing.objects.filter(category=category)
        listing_status = self.request.query_params.get("status", "").strip()
        if listing_status in Listing.Status.values:
            listings = listings.filter(status=listing_status)
        elif listing_status and listing_status not in Listing.Status.values:
            raise ValidationError({"status": ["неизвестный статус объявления"]})
        return listings

    def get(self, request, id):
        serializer = ListingSerializer(self.get_queryset(), many=True)
        return Response(serializer.data)

