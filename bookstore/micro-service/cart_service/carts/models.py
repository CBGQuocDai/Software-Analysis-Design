from django.db import models


class Cart(models.Model):
    customer_id = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Cart {self.id} - Customer {self.customer_id}"


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, related_name='items', on_delete=models.CASCADE)
    book_id = models.IntegerField()
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f"CartItem {self.id} - Book {self.book_id}"
