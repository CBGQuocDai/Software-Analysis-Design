class Cart:
    def __init__(self, id: int, customer_id: int):
        self.id = id
        self.customer_id = customer_id
        self.items = []

    def add_item(self, book, quantity):
        self.items.append((book, quantity))

    def total(self):
        return sum(b.price * q for b, q in self.items)
