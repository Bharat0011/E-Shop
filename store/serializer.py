from rest_framework import serializers
from .models import Product

class ProductSerializer(serializers.ModelSerializer):
    # name = serializers.CharField(max_length=60)
    # price = serializers.IntegerField()
    # description = serializers.CharField(max_length=200)
    # category_name = serializers.CharField(source='category.name')
    class Meta:
        model = Product
        fields = ('name', 'price', 'description', 'image', 'category')
