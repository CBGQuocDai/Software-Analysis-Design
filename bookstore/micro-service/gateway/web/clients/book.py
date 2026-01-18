import requests

BASE = "http://localhost:8002/api/books/"


class BookClient:

    @staticmethod
    def list_books():
        return requests.get(BASE).json()

    @staticmethod
    def get_book(book_id):
        return requests.get(f"{BASE}{book_id}/").json()
