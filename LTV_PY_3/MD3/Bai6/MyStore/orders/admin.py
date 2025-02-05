from django.contrib import admin
from .models import Order,OrderItem
# Register your models here.


class OrderA(admin.ModelAdmin):
    list_display = [field.name for field in Order._meta.fields]
    list_filter = ('address',)
    search_fields = ('address__contains',)

class OrderItemsA(admin.ModelAdmin):
    list_display = [field.name for field in OrderItem._meta.fields]
    list_filter = ('product',)
    search_fields = ('product__contains',)
admin.site.register(Order, OrderA)
admin.site.register(OrderItem, OrderItemsA)
