class CartItem:
    def __init__(self, id: int, cart_id: int, book_id: int, quantity: int):
        self.id = id
        self.cart_id = cart_id
        self.book_id = book_id
        self.quantity = quantity
