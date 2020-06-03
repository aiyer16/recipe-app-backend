from django.test import TestCase
from django.contrib.auth import get_user_model

from .. import models


def sample_user(username='john.smith',
                email='john.smith@gmail.com',
                password='testingpass123'):
    """Create a sample user """
    return get_user_model().\
        objects.create_user(username=username,
                            email=email,
                            password=password)


class ModelsTest(TestCase):

    def test_tag_str(self):
        """Test the tag string representation"""
        tag = models.Tag.objects.create(
            owner=sample_user(),
            name='Vegan'
        )

        self.assertEqual(str(tag), tag.name)

    def test_ingredient_str(self):
        """Test the ingredient string representation"""
        ingredient = models\
            .Ingredient\
            .objects.create(
                owner=sample_user(),
                name='Salt'
            )

        self.assertEqual(str(ingredient), ingredient.name)
