from .models import Cart, CartItem, Order, OrderItem
from rest_framework import serializers

class CartItemSerializer(serializers.ModelSerializer):
    subtotal = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    class Meta:
        model = CartItem
        fields = ['id', 'product', 'quantity', 'subtotal']
    def validate(self, data):
        product = data.get('product')
        quantity = data.get('quantity')
        if product and quantity:
            if quantity > product.stock_quantity:
                raise serializers.ValidationError("Not enough stock available.")
        return data

class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)
    total = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    class Meta:
        model = Cart
        fields = ['id', 'user', 'created_at', 'updated_at', 'items', 'total']

class OrderItemSerializer(serializers.ModelSerializer):
    subtotal = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'product_name', 'price', 'quantity', 'subtotal']

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    class Meta:
        model = Order
        fields = ['id', 'user', 'created_at', 'updated_at', 'status', 'shipping_address', 'total_price', 'items']

class OrderCreateSerializer(serializers.Serializer):
    shipping_address = serializers.CharField(min_length=10)    
    def validate_shipping_address(self, value):
        if not value:
            raise serializers.ValidationError("Shipping address is required.")
        return value
    
class OrderStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['status']
