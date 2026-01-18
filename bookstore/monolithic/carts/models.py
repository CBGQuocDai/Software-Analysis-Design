from django.db import models

class Cart(models.Model):
    customer = models.ForeignKey('accounts.Customer', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)


class CartItem(models.Model):
    cart = models.ForeignKey('carts.Cart', related_name='items', on_delete=models.CASCADE)
    book = models.ForeignKey('books.Book', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
