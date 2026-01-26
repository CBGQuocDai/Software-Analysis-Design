from core.models.book import Book


class BookDAO:
    """Data Access Object for Book model - handles all book-related database operations"""

    @staticmethod
    def get_all_books():
        """
        Retrieve all books from the database
        
        Returns:
            QuerySet: All Book objects
        """
        return Book.objects.all()

    @staticmethod
    def get_book_by_id(book_id):
        """
        Retrieve a single book by ID
        
        Args:
            book_id (int): The ID of the book to retrieve
            
        Returns:
            Book: The Book object or None if not found
        """
        try:
            return Book.objects.get(id=book_id)
        except Book.DoesNotExist:
            return None

    @staticmethod
    def create_book(title, author, price, stock):
        """
        Create a new book in the database
        
        Args:
            title (str): Book title
            author (str): Book author
            price (float): Book price
            stock (int): Stock quantity
            
        Returns:
            Book: The newly created Book object
        """
        book = Book(title=title, author=author, price=price, stock=stock)
        book.save()
        return book

    @staticmethod
    def update_stock(book_id, quantity):
        """
        Update the stock of a book
        
        Args:
            book_id (int): The ID of the book
            quantity (int): The new quantity
        """
        book = BookDAO.get_book_by_id(book_id)
        if book:
            book.stock = quantity
            book.save()
