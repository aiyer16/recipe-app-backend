from rest_framework import serializers
from . import models


class TagSerializer(serializers.ModelSerializer):
    """Serializer for tag object"""
    class Meta:
        model = models.Tag
        fields = ['id', 'name', ]
        read_only_fields = ('id',)


class IngredientSerializer(serializers.ModelSerializer):
    """Serializer for ingredient object"""
    class Meta:
        model = models.Ingredient
        fields = ['id', 'name']
        read_only_fields = ('id',)
