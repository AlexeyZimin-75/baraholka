from typing import Any

from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from .models import Category


class CategorySerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(
        max_length=100, validators=[UniqueValidator(queryset=Category.objects.all(), lookup="iexact")])
    slug = serializers.SlugField(max_length=50,
            validators=[UniqueValidator(queryset=Category.objects.all(), lookup="iexact")])

    def create(self, validated_data: Any):
        return Category.objects.create(**validated_data)

    def update(self, instance, validated_data: Any):
        for field, value in validated_data.items():
            setattr(instance, field, value)
        instance.save()
        return instance

