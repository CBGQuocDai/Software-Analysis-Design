from framework.apps.models import Book as BookModel
from domain.book import Book

class BookRepository:

    def get_all(self):
        books = BookModel.objects.all()
        return [Book(b.id, b.title, b.author, b.price, b.stock) for b in books]

    def get_by_id(self, id):
        b = BookModel.objects.get(id=id)
        return Book(b.id, b.title, b.author, b.price, b.stock)
