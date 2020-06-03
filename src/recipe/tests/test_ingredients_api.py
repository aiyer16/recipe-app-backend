from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

from ..models import Ingredient
from ..serializers import IngredientSerializer

TAGS_URL = reverse('recipe:ingredient-list')


class PublicIngredientAPITests(TestCase):
    """Test the publicly available ingredients API"""

    def setUp(self):
        self.client = APIClient()

    def test_login_required(self):
        """Test that login is required for retrieving ingredients"""
        response = self.client.get(TAGS_URL)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateIngredientAPITests(TestCase:
    """Test the authorized user ingredients API"""

    def setUp(self):
        self.user=get_user_model().objects.create_user(
            username='john.smith',
            password='testing123',
            email='john.smith@gmail.com'
        )
        self.client=APIClient()
        self.client.force_authenticate(self.user)

    def test_retrive_ingredients_auth_success(self):
        """Test retrieving ingredients for authorized user is successful"""
        Ingredient.models.create(owner=self.user, name='Sugar')
        Ingredient.models.create(owner=self.user, name='Salt')

        response=self.client.get(TAGS_URL)
        ingredients=Ingredient.models.all().order_by('-name')
        serializer=IngredientSerializer(ingredients, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assert(response.data, serializer.data)
