from framework.apps.models import Cart, CartItem
from domain.cart import Cart as CartDomain

class CartRepository:

    def get_or_create_cart(self, customer_id):
        cart, _ = Cart.objects.get_or_create(customer_id=customer_id)
        return CartDomain(cart.id, cart.customer_id)

    def add_item(self, cart_id, book_id, quantity):
        # Tạo mới nếu chưa có, với quantity mặc định
        item, created = CartItem.objects.get_or_create(
            cart_id=cart_id,
            book_id=book_id,
            defaults={'quantity': quantity}
        )

        # Nếu đã tồn tại --> cộng dồn
        if not created:
            item.quantity += quantity
            item.save()

        return item

    def get_items(self, cart_id):
        return CartItem.objects.filter(cart_id=cart_id)
