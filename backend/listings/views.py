from rest_framework.response import Response
from rest_framework import status
from .models import Category, Listing
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.exceptions import ValidationError
from .serializers import CategorySerializer

# class CategoryDetail(APIView):
#     def get_object(self, id):
#         return get_object_or_404(Category, id=id)
#
#     def get(self, request, id):
#         return Response(category_to_dict(self.get_object(id)))
#
#     def put(self, request, id):
#         return self.update(request, id, partial=False)
#
#     def patch(self, request, id):
#         return self.update(request, id, partial=True)
#
#     def update(self, request, id, partial):
#         category = self.get_object(id)
#         cleaned, errors = validate_category(request.data, instance=category, partial=partial)
#         if errors:
#             raise ValidationError(errors)
#         for field, value in cleaned.items():
#             setattr(category, field, value)
#         category.save()
#         return Response(category_to_dict(category))
#
#     def delete(self, request, id):
#         category = self.get_object(id)
#         if category.listings.exists():
#             return Response({"detail": "В категории есть объявления"}, status=status.HTTP_409_CONFLICT)
#         category.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)

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

def listing_to_dict(listing):
    return {
        "id": listing.id, "title": listing.title,
        "price": str(listing.price), "city": listing.city,
         "status": listing.status,
        "seller": listing.seller.id,
        "created_at": listing.created_at.isoformat()}



class CategoryListings(APIView):
    def get_queryset(self):
        category = get_object_or_404(Category, id=self.kwargs['id'])
        listings = Listing.objects.filter(category=category)
        listing_status = self.request.query_params.get("status", "").strip()
        if listing_status in Listing.Status.values:
            listings = listings.filter(status=listing_status).order_by('status')
        elif listing_status and listing_status not in Listing.Status.values:
            raise ValidationError({"detail": "неизвестный статус объявления"})
        return listings

    def get(self, request, id):
        return Response([listing_to_dict(listing) for listing in self.get_queryset()])

