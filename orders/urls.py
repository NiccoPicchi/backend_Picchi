from django.urls import path
from .views import CartItemView, CartView, OrderListCreateView, OrderDetailView

urlpatterns = [
    path('cart/', CartView.as_view(), name='cart'),
    path('cart/<int:item_id>/', CartItemView.as_view(), name='cart_item'),
    path('orders/', OrderListCreateView.as_view(), name='order_list_create'),
    path('orders/<int:pk>/', OrderDetailView.as_view(), name='order_detail')
]