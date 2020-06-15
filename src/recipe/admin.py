from django.contrib import admin

from . import models

# Register your models here.
admin.site.register(models.Tag)
admin.site.register(models.Ingredient)
admin.site.register(models.Instruction)
admin.site.register(models.Recipe)
