from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from .models import Category
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.exceptions import ValidationError
from django.db.models import Q

def category_to_dict(category):
    return {"id": category.id, "name": category.name, "slug": category.slug}



def validate_category(data, instance=None, partial=False):
    cleaned, errors = {}, {}
    for field in ("name", "slug"):
        if field not in data:
            if not partial:
                errors[field] = ["обязательное поле"]
            continue
        value = str(data[field]).strip()
        if not value:
            errors[field] = ["поле не может быть пустым"]
            continue
        if len(value) > Category._meta.get_field(field).max_length:
            errors[field] = ["значение поля слишком большое"]
            continue

        taken = Category.objects.filter(**{field: value})
        if instance is not None:
            taken = taken.exclude(id=instance.id)
        if taken.exists():
            errors[field] = ["поле уже занято"]
            continue

        cleaned[field] = value
    return cleaned, errors

class CategoryDetail(APIView):
    def get_object(self, id):
        return get_object_or_404(Category, id=id)

    def get(self, request, id):
        return Response(category_to_dict(self.get_object(id)))

    def put(self, request, id):
        return self.update(request, id, partial=False)

    def patch(self, request, id):
        return self.update(request, id, partial=True)

    def update(self, request, id, partial):
        category = self.get_object(id)
        cleaned, errors = validate_category(request.data, instance=category, partial=partial)
        if errors:
            raise ValidationError(errors)
        for field, value in cleaned.items():
            setattr(category, field, value)
        category.save()
        return Response(category_to_dict(category))

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
            categories = categories.filter(
                Q(name__icontains=search) | Q(slug__icontains=search)
            )
        return categories

    def get(self, request):
        return Response([category_to_dict(category) for category in self.get_queryset()])

    def post(self, request):
        cleaned, errors = validate_category(request.data)
        if errors:
            raise ValidationError(errors)
        category = Category.objects.create(**cleaned)
        return Response(category_to_dict(category), status=status.HTTP_201_CREATED)






