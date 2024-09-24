from django.contrib.auth import get_user_model

from rest_framework.test import APIClient
from rest_framework import status

from django.urls import reverse
from django.test import TestCase

from recipe.serializer import IngredientSerializer
from core.models import Ingredient


def create_user(email='user@example.com', password='testpass123'):
    return get_user_model().objects.create_user(email=email, password=password)


def detail_url(ingredient_id):
    """Create and return a tag detail url"""
    return reverse('recipe:ingredient-detail', args=[ingredient_id])


INGREDIENT_URL = reverse('recipe:ingredient-list')


class PublicIngredientApiTests(TestCase):

    def setUp(self) -> None:
        self.client = APIClient()

    def test_auth_required(self):
        """Test auth is required for retrieving ingredeints"""
        res = self.client.get(INGREDIENT_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateIngredientApiTests(TestCase):

    def setUp(self) -> None:
        self.client = APIClient()
        self.user = create_user(email='test1@example.com',
                                password='testpass123')
        self.client.force_authenticate(self.user)

    def test_create_ingredient(self):
        payload = {'name': 'Watermelon'}
        res = self.client.post(INGREDIENT_URL, payload)
        ingredients = Ingredient.objects.filter(user=self.user)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(ingredients.count(), 1)
        self.assertIn(payload['name'], ingredients.first().name)

    def test_create_ingredient_invalid(self):
        payload = {'name': ''}
        res = self.client.post(INGREDIENT_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Ingredient.objects.filter(user=self.user).count(), 0)

    def test_delete_ingredient(self):
        ingredient = Ingredient.objects.create(user=self.user,
                                               name='Coriander')
        url = detail_url(ingredient.id)
        res = self.client.delete(url)
        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Ingredient.objects.filter(user=self.user).count(), 0)

    def test_update_ingredient(self):
        ingredient = Ingredient.objects.create(user=self.user, name="Love")
        url = detail_url(ingredient.id)
        payload = {'name': "The thing I need money for"}
        res = self.client.patch(url, payload)
        print(f'content: {res.content}')
        print(f'data: {res.data}')
        self.assertEqual(res.status_code, status.HTTP_200_OK)

        ingredients = Ingredient.objects.filter(user=self.user)

        self.assertEqual(str(ingredients[0]), payload['name'])

    def test_retrieve_ingredients_list(self):
        """Test retreving a list of ingredients"""
        Ingredient.objects.create(user=self.user, name="Pineapple")
        Ingredient.objects.create(user=self.user, name="Kale")

        res = self.client.get(INGREDIENT_URL)

        ingredients = Ingredient.objects.all().order_by('-id')
        serializer = IngredientSerializer(ingredients, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_ingredients_limited_to_user(self):
        other_user = create_user(email="poop@example.com", password="yayayya")

        Ingredient.objects.create(user=other_user, name="Kale")
        Ingredient.objects.create(user=self.user, name="Notkale")
        res = self.client.get(INGREDIENT_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        ingredient = Ingredient.objects.filter(user=self.user)

        serialized = IngredientSerializer(ingredient, many=True)
        self.assertEqual(res.data, serialized.data)
