from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

from ..models import Ingredient
from ..serializers import IngredientSerializer

INGREDIENTS_URL = reverse('recipe:ingredient-list')


class PublicIngredientAPITests(TestCase):
    """Test the publicly available ingredients API"""

    def setUp(self):
        self.client = APIClient()

    def test_login_required(self):
        """Test that login is required for retrieving ingredients"""
        response = self.client.get(INGREDIENTS_URL)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateIngredientAPITests(TestCase):
    """Test the authorized user ingredients API"""

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='john.smith',
            password='testing123',
            email='john.smith@gmail.com'
        )
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_retrive_ingredients_auth_success(self):
        """Test retrieving ingredients for authorized user is successful"""
        Ingredient.objects.create(owner=self.user, name='Sugar')
        Ingredient.objects.create(owner=self.user, name='Salt')

        response = self.client.get(INGREDIENTS_URL)
        ingredients = Ingredient.objects.all().order_by('name')
        serializer = IngredientSerializer(ingredients, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_retrive_ingredients_limited_to_user(self):
        """Test retrieving ingredients limited to user making request"""
        user2 = get_user_model().objects.create_user(
            username='jane.doe',
            password='testing1234',
            email='jane.doe@gmail.com'
        )

        # Create ingredient tied to new user
        Ingredient.objects.create(
            owner=user2,
            name='Red Chillies'
        )

        # Create ingredient tied to original user
        ingredient = Ingredient.objects.create(
            owner=self.user,
            name='Sugar'
        )

        response = self.client.get(INGREDIENTS_URL)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], ingredient.name)

    def test_create_invalid_ingredient_fail(self):
        """Test creating a new ingredient with invalid payload fails"""

        payload = {'name': ''}
        response = self.client.post(INGREDIENTS_URL, payload)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
