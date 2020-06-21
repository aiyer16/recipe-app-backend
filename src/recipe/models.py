from django.db import models
from django.conf import settings


class OwnerModel(models.Model):
    """Model for owner. Cascaded to other models"""
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )

    class Meta:
        abstract = True


class Tag(OwnerModel):
    """Tag to be used for a recipe"""

    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Ingredient(OwnerModel):
    """Ingredient to be used for a recipe"""

    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Instruction(models.Model):
    """Instruction to make a recipe"""

    recipe = models.ForeignKey(
        'Recipe', related_name='instructions', on_delete=models.CASCADE)

    order = models.IntegerField()
    description = models.TextField()
    duration_in_min = models.IntegerField(null=True)

    def __str__(self):
        return f'{str(self.order)}: {self.description}'

    class Meta:
        unique_together = ['recipe', 'order']


class Recipe(OwnerModel):
    """Core Recipe Model"""
    title = models.CharField(max_length=255)
    time_in_minutes = models.IntegerField()
    ingredients = models.ManyToManyField('Ingredient')
    tags = models.ManyToManyField('Tag')

    def __str__(self):
        return self.title
