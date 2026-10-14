from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from .models import Category
from django.shortcuts import get_object_or_404

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

@api_view(["GET", "PUT", "PATCH", "DELETE"])
def category_detail(request, id):
    category = get_object_or_404(Category, id=id)
    if request.method == "GET":
        return Response(category_to_dict(category))

    if request.method == "DELETE":
        if category.listings.exists():
            return Response({"detail": "в категории есть объявления"}, status=status.HTTP_409_CONFLICT)
        category.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    partial = request.method == "PATCH"
    cleaned, errors = validate_category(request.data, instance=category, partial=partial)
    if errors:
        return Response(errors, status=status.HTTP_400_BAD_REQUEST)
    for field, value in cleaned.items():
        setattr(category, field, value)
    category.save()
    return Response(category_to_dict(category))


@api_view(["GET", "POST"])
def category_list(request):
    if request.method == "GET":
        categories = Category.objects.all()
        search = request.query_params.get("search", "").strip()
        if search:
            categories = categories.filter(name__icontains=search)
        return Response([category_to_dict(category) for category in categories])

    cleaned, errors = validate_category(request.data)
    if errors:
        return Response(errors, status=status.HTTP_400_BAD_REQUEST)
    new_category = Category.objects.create(**cleaned)
    return Response(category_to_dict(new_category), status=status.HTTP_201_CREATED)





