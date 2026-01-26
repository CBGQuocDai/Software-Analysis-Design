from django.db import models
from .customer import Customer


class Cart(models.Model):
    """Cart model representing a shopping cart for a customer"""
    id = models.AutoField(primary_key=True)
    customer = models.OneToOneField(Customer, on_delete=models.CASCADE, related_name='cart')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        app_label = 'core'
        db_table = 'core_cart'

    def __str__(self):
        return f"Cart for {self.customer.name}"
