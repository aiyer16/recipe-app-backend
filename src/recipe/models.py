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
