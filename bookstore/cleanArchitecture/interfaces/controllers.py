from usecases.accounts.register import RegisterCustomer
from usecases.accounts.login import LoginCustomer
from usecases.books.view_books import ViewBooks
from usecases.carts.add_item import AddItem
from usecases.carts.view_cart import ViewCart

def register(data):
    return RegisterCustomer().execute(**data)

def login(data):
    return LoginCustomer().execute(**data)

def list_books():
    return ViewBooks().execute()

def add_to_cart(customer_id, book_id, qty):
    AddItem().execute(customer_id, book_id, qty)

def view_cart(customer_id):
    return ViewCart().execute(customer_id)
