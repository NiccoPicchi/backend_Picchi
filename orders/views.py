from .serializers import CartSerializer, CartItemSerializer, OrderSerializer, OrderCreateSerializer, OrderStatusSerializer
from .models import Cart, CartItem, Order, OrderItem
from rest_framework import status
from rest_framework.response import Response
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from accounts.permissions import IsCustomer, IsManager
from django.shortcuts import get_object_or_404
# Create your views here.
class CartView(generics.GenericAPIView):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    permission_classes = [IsCustomer]

    def get(self, request):
        cart, created = Cart.objects.get_or_create(user=request.user)
        serializer = CartSerializer(cart)
        return Response(serializer.data)
    
    def post(self, request):
        cart, created = Cart.objects.get_or_create(user=request.user)
        serializer = CartItemSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
    
        product = serializer.validated_data['product']
        quantity = serializer.validated_data['quantity']
    
        cart_item, item_created = CartItem.objects.get_or_create(
            cart=cart,
            product=product,
            defaults={'quantity': quantity}
        )   
    
        if not item_created:
            new_quantity = cart_item.quantity + quantity
            if new_quantity > product.stock_quantity:
                return Response(
                    {"error": "Not enough stock available."},
                    status=status.HTTP_400_BAD_REQUEST
                )
            cart_item.quantity = new_quantity
            cart_item.save()
        return Response(CartItemSerializer(cart_item).data, status=status.HTTP_201_CREATED)
    
    def delete(self, request):
        cart, created = Cart.objects.get_or_create(user=request.user)
        cart.items.all().delete()
        return Response({"message": "Cart cleared"}, status=status.HTTP_204_NO_CONTENT)
    
class CartItemView(generics.GenericAPIView):
    permission_classes = [IsCustomer]
        
    def patch(self, request, item_id):
        try:
            cart_item = CartItem.objects.get(id=item_id, cart__user=request.user)
        except CartItem.DoesNotExist:                return Response({"error": "Cart item not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = CartItemSerializer(cart_item, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
        
    def delete(self, request, item_id): 
        try:
            cart_item = CartItem.objects.get(id=item_id, cart__user=request.user)
        except CartItem.DoesNotExist:
            return Response({"error": "Cart item not found"}, status=status.HTTP_404_NOT_FOUND)
        cart_item.delete()
        return Response({"message": "Cart item removed"}, status=status.HTTP_204_NO_CONTENT)
        
class OrderListCreateView(generics.ListCreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if self.request.user.is_manager:
            orders = Order.objects.all()
        else:
            orders = Order.objects.filter(user=self.request.user)
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)
        
        
    def post(self, request):
        serializer = OrderCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        if request.user.is_customer:
            cart = get_object_or_404(Cart, user=request.user)
            if not cart.items.exists():
                return Response({"error": "Cart is empty"}, status=status.HTTP_400_BAD_REQUEST)
            for item in cart.items.all():
                if item.quantity > item.product.stock_quantity:
                    return Response({"error": f"Not enough stock for {item.product.name}"}, status=status.HTTP_400_BAD_REQUEST)
            order = Order.objects.create(user=request.user, shipping_address=request.data.get('shipping_address'), total_price=cart.total())
            for item in cart.items.all():
                OrderItem.objects.create(order=order, product=item.product, product_name=item.product.name, quantity=item.quantity, price=item.product.price)
                item.product.stock_quantity -= item.quantity
                item.product.save()
            cart.items.all().delete()
            serializer = OrderSerializer(order)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response({"error": "Invalid data"}, status=status.HTTP_400_BAD_REQUEST)


class OrderDetailView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        order = get_object_or_404(Order, pk=pk)
        if request.user != order.user and not request.user.is_customer() and not request.user.is_manager():
            return Response({"error": "You do not have permission to view this order"}, status=status.HTTP_403_FORBIDDEN)
        serializer = OrderSerializer(order)
        return Response(serializer.data)


        
    def patch(self, request, pk):
        if request.user.is_manager():
            order = get_object_or_404(Order, pk=pk)
            serializer = OrderStatusSerializer(order, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(OrderSerializer(order).data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"error": "You do not have permission to update this order"}, status=status.HTTP_403_FORBIDDEN)
            
    def delete(self, request, pk):
        if request.user.is_customer:
            order = get_object_or_404(Order, pk=pk, user=request.user)
            if order.status != 'PENDING':
                return Response({"error": "Only pending orders can be cancelled"}, status=status.HTTP_400_BAD_REQUEST)
            order.status = 'CANCELLED'
            order.save()
            return Response({"message": "Order cancelled"}, status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({"error": "You do not have permission to cancel this order"}, status=status.HTTP_403_FORBIDDEN)
            


