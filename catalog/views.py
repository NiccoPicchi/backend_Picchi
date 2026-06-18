from catalog.serializers import CategorySerializer, ProductSerializer
from .models import Product, Category
from accounts.permissions import IsManagerOrReadOnly
from rest_framework import viewsets


# Create your views here.
class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsManagerOrReadOnly,)

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = (IsManagerOrReadOnly,)

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
        ordering = self.request.query_params.get("ordering")
        ALLOWED_ORDERING = ['price', '-price', 'name', '-name', 'id', '-id']
        if ordering and ordering in ALLOWED_ORDERING:
            queryset = queryset.order_by(ordering)
        return queryset

