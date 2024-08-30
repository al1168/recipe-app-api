from django.contrib.auth import get_user_model

from rest_framework.test import APIClient
from rest_framework import status

from django.urls import reverse
from django.test import TestCase

from core.models import Ingredient


def create_user(email='user@example.com', password='testpass123'):
    return get_user_model().objects.create_user(email=email, password=password)


def detail_url(ingredient_id):
    """Create and return a tag detail url"""
    return reverse('recipe:ingredient-detail', args=[ingredient_id])


INGREDIENT_URL = reverse('recipe:ingredient-list')


class PublicIngredientApiTests(TestCase):

    def test_create_ingredient(self):
        pass


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

    def update_ingredient(self):
        ingredient = Ingredient.objects.create(user=self.user,
                                               name='Coriander')
        payload = {'name': 'Coriander'}
        url = detail_url(ingredient.id)
        res = self.client.patch(url, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        ingredient.refresh_from_db()
        self.assertEqual(ingredient.name, payload['name'])

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
