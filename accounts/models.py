from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class CustomUser(AbstractUser):
    CUSTOMER = 'customer'
    MANAGER = 'manager'
    ROLE_CHOICES = [
        (CUSTOMER, 'Customer'),
        (MANAGER, 'Manager'),
    ]
    role = models.CharField(max_length=50, blank=False, null=False, choices=ROLE_CHOICES, default=CUSTOMER)
    address = models.CharField(max_length=255, blank=True, null=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    def is_customer(self):
        return self.role == self.CUSTOMER
    def is_manager(self):
        return self.role == self.MANAGER
