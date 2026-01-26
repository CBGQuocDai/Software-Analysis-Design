from __future__ import annotations

from django.db import models


class Cart(models.Model):
    customer = models.ForeignKey("store.Customer", on_delete=models.CASCADE, related_name="carts")
    is_active = models.BooleanField(default=True)

    def __str__(self) -> str:
        return f"Cart({self.id}) for {self.customer_id}"


class CartItem(models.Model):
    cart = models.ForeignKey("store.Cart", on_delete=models.CASCADE, related_name="items")
    quantity = models.IntegerField(default=1)
    book = models.ForeignKey("store.Book", on_delete=models.CASCADE, related_name="cart_items")

    class Meta:
        unique_together = ("cart", "book")

    def __str__(self) -> str:
        return f"CartItem({self.id}): {self.book_id} x{self.quantity}"

    @classmethod
    def addItem(cls, *, cart: "Cart", book: "Book", quantity: int = 1) -> "CartItem":
        item, created = cls.objects.get_or_create(cart=cart, book=book, defaults={"quantity": quantity})
        if not created:
            item.quantity += quantity
            item.save(update_fields=["quantity"])
        return item


class Order(models.Model):
    customer = models.ForeignKey("store.Customer", on_delete=models.CASCADE, related_name="orders")
    total_price = models.FloatField(default=0.0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"Order({self.id}) for {self.customer_id}"

    @classmethod
    def createOrder(cls, *, customer: "Customer", total_price: float = 0.0) -> "Order":
        return cls.objects.create(customer=customer, total_price=total_price)


class Payment(models.Model):
    order = models.OneToOneField("store.Order", on_delete=models.CASCADE, related_name="payment")
    method_name = models.CharField(max_length=100)
    status = models.CharField(max_length=50, default="pending")

    def __str__(self) -> str:
        return f"Payment({self.method_name}, {self.status})"


class Shipping(models.Model):
    order = models.ForeignKey("store.Order", on_delete=models.CASCADE, related_name="shippings")
    fee = models.FloatField(default=0.0)
    method_name = models.CharField(max_length=100)

    def __str__(self) -> str:
        return f"Shipping({self.method_name}, fee={self.fee})"
