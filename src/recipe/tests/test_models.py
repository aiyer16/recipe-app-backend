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

    def test_recipe_str(self):
        """Test the recipe string representation"""
        recipe = models.Recipe.objects.create(
            owner=sample_user(),
            title='Paneer Makhani',
            time_in_minutes=5
        )

        self.assertEqual(str(recipe), recipe.title)

    def test_instruction_str(self):
        """Test the instruction string representation"""
        recipe = models.Recipe.objects.create(
            owner=sample_user(),
            title='Paneer Makhani',
            time_in_minutes=5
        )

        instruction = models.Instruction.objects.create(
            recipe=recipe,
            order=1,
            description="Add 2tbsp. oil",
        )

        self.assertEqual(str(instruction),
                         str(instruction.order) +
                         ': ' + instruction.description)
