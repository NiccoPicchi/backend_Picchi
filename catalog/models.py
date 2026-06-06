from django.db import models

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=100, blank=False, null=False)
    description = models.TextField(blank=True)
    class Meta:
        ordering = ['name']
    def __str__(self):
        return self.name
    
class Product(models.Model):
    name = models.CharField(max_length=100, blank=False, null=False)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    available = models.BooleanField(default=True)
    stock_quantity = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        ordering = ['name']
    def __str__(self):
        return self.name
    def save(self, *args, **kwargs):
        if self.stock_quantity > 0:
            self.available = True
        elif self.stock_quantity == 0:
            self.available = False
        super().save(*args, **kwargs)