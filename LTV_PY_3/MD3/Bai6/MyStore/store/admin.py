from django.contrib import admin

# Register your models here.
from .models import Category, SubCategory, Product, Customer, UserProfileInfo

admin.site.register(Category)
admin.site.register(SubCategory)
admin.site.register(Customer)
admin.site.register(UserProfileInfo)

class ProductA(admin.ModelAdmin):
    list_display = ('name', 'price', 'public_day', 'viewed')
    list_filter = ('public_day', 'subcategory')
    search_fields = ('name__contains',)
admin.site.register(Product, ProductA)
admin.site.site_header = "My Store Admin"