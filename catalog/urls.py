from django.urls import path
from .views import CategoryViewSet, ProductViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r"categories", CategoryViewSet)
router.register(r"products", ProductViewSet)
urlpatterns = router.urls