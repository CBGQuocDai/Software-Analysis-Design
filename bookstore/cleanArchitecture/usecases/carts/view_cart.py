from infrastructure.repositories.cart_repo import CartRepository

class ViewCart:

    def execute(self, customer_id):
        repo = CartRepository()

        cart = repo.get_or_create_cart(customer_id)

        return repo.get_items(cart.id)