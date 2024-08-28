from django.contrib.auth import get_user_model

from django.urls import reverse
from unittest import TestCase


def create_user():
    return get_user_model().objects.create(
        email="test@example.com",
        password="1234qwer")


def detail_url(tag_id):
    """Create and return a tag detail url"""
    return reverse('recipe:tag-detail', args=[tag_id])


INGREDIENT_URL = reverse('recipe:ingredient-list')


class PublicIngredientApiTests(TestCase):

    def test_create_ingredient(self):
        pass
