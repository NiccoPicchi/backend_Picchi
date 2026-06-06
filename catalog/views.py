from unicodedata import name

from catalog.serializers import CategorySerializer, ProductSerializer
from .models import Product, Category
from accounts.permissions import IsManagerOrReadOnly
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

# Create your views here.
class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsManagerOrReadOnly]

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsManagerOrReadOnly]

    def get_queryset(self):
        queryset = Product.objects.all()
        user = self.request.user
        if not (user.is_authenticated and user.is_manager()):
            queryset = queryset.filter(available=True)
        name = self.request.query_params.get("name")
        category_id = self.request.query_params.get("category")
        category_name = self.request.query_params.get("category_name")
        product_id = self.request.query_params.get("id")
        if name:
            queryset = queryset.filter(name__icontains=name)
        if category_id:
            queryset = queryset.filter(category__id=category_id)
        if category_name:
            queryset = queryset.filter(category__name__icontains=category_name)
        if product_id:
            queryset = queryset.filter(id=product_id)
        return queryset

    @action(detail=False, methods=["get"], permission_classes=[AllowAny])
    def available(self, request):
        queryset = Product.objects.filter(available=True)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
