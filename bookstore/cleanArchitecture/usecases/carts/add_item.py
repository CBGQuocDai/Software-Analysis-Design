from infrastructure.repositories.cart_repo import CartRepository
from infrastructure.repositories.book_repo import BookRepository
class AddItem:

    def execute(self, customer_id, book_id, quantity):
        repo = CartRepository()

        cart = repo.get_or_create_cart(customer_id)
        book = BookRepository().get_by_id(book_id)
        if book.stock < quantity:
            raise Exception("Not enough stock available")
        repo.add_item(cart.id, book_id, quantity)
