from rest_framework import serializers
from .models import Product, Category

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'description']

class ProductSerializer(serializers.ModelSerializer):
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all())
    category_name = serializers.CharField(source='category.name', read_only=True)
    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'price', 'category', 'category_name', 'available', 'stock_quantity', 'created_at', 'updated_at']

    def validate_price(self, value):
        if value <= 0:
            raise serializers.ValidationError("Price must be a positive number.")
        return value
    
    def validate_stock(self, value):
        if value < 0:
            raise serializers.ValidationError("Stock must be a non-negative integer.")
        return value