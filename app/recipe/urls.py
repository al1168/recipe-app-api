"""
URL mappings for the recipe app.
"""
from django.urls import (
    path,
    include,
)

from rest_framework.routers import DefaultRouter

from recipe import views


router = DefaultRouter()
router.register('recipes', views.RecipeViewSet)
router.register('tags', views.TagViewSet)
router.register('Ingredients', views.IngredientViewSet)
app_name = 'recipe'

urlpatterns = [
    path('', include(router.urls)),
    path('recipes/<int:pk>/remove-ingredient/<int:ingredient_id>/',
         views.RecipeViewSet.as_view(
            {'patch': 'remove_ingredient'}
            ),
         name='remove-ingredient'),
    path('recipes/<int:pk>/add-ingredient/<int:ingredient_id>/',
         views.RecipeViewSet.as_view(
            {'patch': 'add_ingredient'}
            ),
         name='add-ingredient')
]
