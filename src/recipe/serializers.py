from rest_framework import serializers
from . import models


class TagSerializer(serializers.ModelSerializer):
    """Serializer for tag object"""
    class Meta:
        model = models.Tag
        fields = ['id', 'name', ]
        read_only_fields = ('id',)


class IngredientSerializer(serializers.ModelSerializer):
    """Serializer for ingredient object"""
    class Meta:
        model = models.Ingredient
        fields = ['id', 'name']
        read_only_fields = ('id',)


class InstructionSerializer(serializers.ModelSerializer):
    """Serializer for instruction object"""
    class Meta:
        model = models.Instruction
        fields = ['order', 'description', 'duration_in_min']


class RecipeSerializer(serializers.ModelSerializer):
    """Serializer for recipe object"""

    # Using serializer here so that nested fields can be shown
    # with full information in list view (GET request)
    ingredients = IngredientSerializer(many=True, read_only=True)
    tags = TagSerializer(many=True, read_only=True)
    instructions = InstructionSerializer(many=True)

    class Meta:
        model = models.Recipe
        fields = ['id',
                  'title',
                  'time_in_minutes',
                  'ingredients',
                  'instructions',
                  'tags']
        read_only_fields = ('id',)


class RecipeCreateSerializer(RecipeSerializer):
    """Serializer for recipe object create operations"""

    # Override ingredient and tag fields to make them writable via foreign keys
    ingredients = serializers.PrimaryKeyRelatedField(
        many=True, queryset=models.Ingredient.objects.all())

    tags = serializers.PrimaryKeyRelatedField(
        many=True, queryset=models.Tag.objects.all()
    )

    def create(self, validated_data):
        """Override create method to save nested serializer"""

        # Pop out instruction, ingredient and tag fields from form data
        # We'll handle inserting these fields manually
        instruction_validated_data = validated_data.pop('instructions')
        ingredient_validated_data = validated_data.pop('ingredients')
        tag_validated_data = validated_data.pop('tags')

        # Create an instance of the recipe object without the instruction,
        # tag and ingredient fields. These will be set later.
        recipe = models.Recipe.objects.create(**validated_data)

        # Insert instructions to recipe_instructions table manually
        instruction_serializer = self.fields['instructions']

        # Attach recipe object created before to recipe_instruction.recipe
        for instruction in instruction_validated_data:
            instruction['recipe'] = recipe

        # Create an instance of the instruction object
        instructions = instruction_serializer.create(
            instruction_validated_data)

        # Get the corrsponding ingredients and tag fields based on key
        ingredients = models.Ingredient.objects.filter(
            name__in=ingredient_validated_data)
        tags = models.Tag.objects.filter(name__in=tag_validated_data)

        # Now set the ingredient and tag field for recipe object
        recipe.ingredients.set(ingredients)
        recipe.tags.set(tags)

        # Finally return the recipe serializer
        return recipe
