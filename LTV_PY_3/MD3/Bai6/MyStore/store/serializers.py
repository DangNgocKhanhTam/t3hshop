from .models import Product, SubCategory
from rest_framework import serializers

class ProductSerializer(serializers.HyperlinkedModelSerializer):
    subcategory = serializers.CharField(source = 'subcategory.id')
    class Meta: 
        model = Product
        fields = '__all__'