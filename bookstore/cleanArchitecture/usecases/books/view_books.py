from infrastructure.repositories.book_repo import BookRepository

class ViewBooks:

    def execute(self):
        repo = BookRepository()
        return repo.get_all()
