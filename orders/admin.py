from django.contrib import admin

# Register your models here.
from .models import Cart, CartItem, Order, OrderItem

admin.site.register(Order)
admin.site.register(OrderItem)