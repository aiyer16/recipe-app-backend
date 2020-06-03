from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

from ..models import Tag
from ..serializers import TagSerializer

TAGS_URL = reverse('recipe:tag-list')


class PublicTagsAPITests(TestCase):
    """Test the publicly available tags API"""

    def setUp(self):
        self.client = APIClient()

    def test_login_required(self):
        """Test login is required for retrieving tags"""
        response = self.client.get(TAGS_URL)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateTagsAPITests(TestCase):
    """Test the authorized user tags API"""

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='john.smith',
            email='john.smith@gmail.com',
            password='testing123'
        )
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_retrieve_tags_success(self):
        """Test retrieving tags works"""
        Tag.objects.create(owner=self.user, name='Vegan')
        Tag.objects.create(owner=self.user, name='Dessert')

        response = self.client.get(TAGS_URL)
        tags = Tag.objects.all().order_by('name')
        serializer = TagSerializer(tags, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_retrieved_tags_limited_to_user(self):
        """Test that tags returned are for the authenticated user"""

        # First let's create a new user, so that we can ultimately
        # create 2 tags in the system - one for each user
        user_2 = get_user_model().objects.create_user(
            username='jane.doe',
            email='jane.doe@gmail.com',
            password='testingpass123'
        )

        # Create tag tied to new user
        Tag.objects.create(owner=user_2, name='Fruity')

        # Create tag tied to original user
        tag = Tag.objects.create(owner=self.user, name='Indian')

        response = self.client.get(TAGS_URL)

        # We're authenticating with original user only, so we should
        # only get one tag in the response.
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], tag.name)

    def test_create_tag_success(self):
        """Test creating a new tag"""

        payload = {'name': 'TestTag'}
        self.client.post(TAGS_URL, payload)

        exists = Tag.objects.filter(
            owner=self.user,
            name=payload['name']
        ).exists()

        self.assertTrue(exists)

    def test_create_invalid_tag_fail(self):
        """Test creating a new tag with invalid payload fails"""

        payload = {'name': ''}
        response = self.client.post(TAGS_URL, payload)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
