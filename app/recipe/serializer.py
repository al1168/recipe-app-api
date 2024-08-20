"""
Serializer for Recipes
"""
from rest_framework.serializers import ModelSerializer

from core.models import Recipe


class RecipeSerializer(ModelSerializer):
    """Serializer for Recipes"""
    class Meta:
        model = Recipe
        fields = ['id', 'title', 'time_minutes', ]
    # def create():
    #     pass

    # def update():
    #     pass
