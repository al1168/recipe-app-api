"""
Serializer for Recipes
"""
from rest_framework.serializers import ModelSerializer

from core.models import (
    Recipe,
    Tag,
    Ingredient
)


class IngredientSerializer(ModelSerializer):

    class Meta:
        model = Ingredient
        fields = ['id', 'name']
        read_only_fields = ['id']

    def validate_name(self, value):
        if value.strip() == '':
            raise ValueError("Ingredient name must not be empty")
        return value


class TagSerializer(ModelSerializer):
    """Serialzer for tags"""

    class Meta:
        model = Tag
        fields = ['id', 'name']
        read_only_fields = ['id']


class RecipeSerializer(ModelSerializer):
    """Serializer for Recipes"""
    tags = TagSerializer(many=True, required=False)
    ingredients = IngredientSerializer(many=True, required=False)

    class Meta:
        model = Recipe
        fields = ['id', 'title', 'time_minutes',
                  'price', 'link', 'tags', 'ingredients']

    def _get_or_create_item(self, tags, recipe, Type):
        auth_user = self.context['request'].user
        obj = Type
        for tag in tags:
            tag_obj, created = obj.objects.get_or_create(
                user=auth_user,
                **tag
            )
            recipe.tags.add(tag_obj)
            if created:
                print(f"new tag {tag} was created")

    def create(self, validated_data):
        """Create a recipe"""
        tags = validated_data.pop('tags', [])
        ingredients = validated_data.pop('ingredients', [])
        recipe = Recipe.objects.create(**validated_data)
        self._get_or_create_item(tags, recipe, Tag)
        self._get_or_create_item(ingredients, recipe, Ingredient)
        return recipe

    def update(self, instance, validated_data):
        """Update recipe."""
        tags = validated_data.pop('tags', None)
        if tags is not None:
            instance.tags.clear()
            self._get_or_create_item(tags, instance, Tag)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance


class RecipleDetailSerializer(RecipeSerializer):
    """Serializer for recipe detail view."""

    class Meta(RecipeSerializer.Meta):
        fields = RecipeSerializer.Meta.fields + ['description']
