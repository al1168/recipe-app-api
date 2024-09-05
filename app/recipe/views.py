"""
Views for recipe APIs.
"""
from rest_framework import (
    viewsets,
    mixins,
    status
    )
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action
from core.models import (
    Recipe,
    Tag,
    Ingredient
)

from recipe import serializer
from django.shortcuts import get_object_or_404


class RecipeViewSet(viewsets.ModelViewSet):
    """View for manage recipe APis."""
    serializer_class = serializer.RecipleDetailSerializer
    queryset = Recipe.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Retrieve recipes for authenticated user."""
        return self.queryset.filter(user=self.request.user).order_by('-id')

    def get_serializer_class(self):
        """Return the serializer class for request."""
        if self.action == 'list':
            return serializer.RecipeSerializer

        return self.serializer_class

    def perform_create(self, serializer):
        """Create a new recipe"""
        serializer.save(user=self.request.user)

    @action(methods=['DELETE'], detail=True)
    def remove_ingredient(self, request, pk=None, ingredient_id=None):
        """Remove an ingredient from a recipe."""
        recipe = self.get_object()
        ingredient = get_object_or_404(Ingredient, id=ingredient_id)
        recipe.ingredients.remove(ingredient)
        return Response(status=status.HTTP_204_NO_CONTENT)


class TagViewSet(mixins.ListModelMixin,
                 mixins.UpdateModelMixin,
                 mixins.DestroyModelMixin,
                 viewsets.GenericViewSet):
    """Manage tags in the database."""
    serializer_class = serializer.TagSerializer
    queryset = Tag.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Filter querset to authenticated user"""
        return self.queryset.filter(user=self.request.user).order_by('-name')


class IngredientViewSet(mixins.ListModelMixin, mixins.CreateModelMixin,
                        mixins.DestroyModelMixin, mixins.UpdateModelMixin,
                        viewsets.GenericViewSet):
    """Manage Ingredient in the database"""

    serializer_class = serializer.IngredientSerializer
    queryset = Ingredient.objects.all()
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def get_queryset(self):
        """Filter querset to authenticated user"""

        return self.queryset.filter(user=self.request.user).order_by('-name')

    def perform_create(self, serializer):
        """Create a new recipe"""
        serializer.save(user=self.request.user)
