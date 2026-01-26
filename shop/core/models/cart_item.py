from django.db import models
from django.core.validators import MinValueValidator
from .cart import Cart
from .book import Book


class CartItem(models.Model):
    """CartItem model representing an item in a shopping cart"""
    id = models.AutoField(primary_key=True)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    quantity = models.IntegerField(validators=[MinValueValidator(1)])
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        app_label = 'core'
        db_table = 'core_cart_item'
        unique_together = ('cart', 'book')

    def __str__(self):
        return f"{self.quantity}x {self.book.title} in {self.cart}"
