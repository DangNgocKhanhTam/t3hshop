from django.contrib import admin

# Register your models here.
from .models import Category, Story

admin.site.register(Category)
admin.site.register(Story)

