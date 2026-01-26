import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'app.settings')
django.setup()

from store.models import Book, Customer, Rating

def seed_data():
    print("Seeding 50 books and sample data...")
    
    # 1. Create Customers
    c1, _ = Customer.objects.get_or_create(id="c1", defaults={"name": "Nguyen Van A", "email": "ana@example.com", "password": "123"})
    c2, _ = Customer.objects.get_or_create(id="c2", defaults={"name": "Tran Thi B", "email": "bibi@example.com", "password": "123"})
    
    # 2. Create 50 Books
    base_books = [
        ("Clean Code", "Robert C. Martin", 45.0),
        ("The Pragmatic Programmer", "Andrew Hunt", 50.0),
        ("Design Patterns", "Gang of Four", 55.0),
        ("Python Crash Course", "Eric Matthes", 35.0),
        ("Introduction to Algorithms", "CLRS", 90.0),
        ("Deep Learning", "Ian Goodfellow", 80.0),
        ("Atomic Habits", "James Clear", 25.0),
        ("The Psychology of Money", "Morgan Housel", 20.0),
        ("Refactoring", "Martin Fowler", 48.0),
        ("Code Complete", "Steve McConnell", 52.0),
        ("Head First Design Patterns", "Eric Freeman", 42.0),
        ("You Don't Know JS", "Kyle Simpson", 30.0),
        ("Effective Java", "Joshua Bloch", 40.0),
        ("Clean Architecture", "Robert C. Martin", 44.0),
        ("Test Driven Development", "Kent Beck", 38.0),
        ("Domain-Driven Design", "Eric Evans", 60.0),
        ("Hackers & Painters", "Paul Graham", 22.0),
        ("Zero to One", "Peter Thiel", 28.0),
        ("The Lean Startup", "Eric Ries", 26.0),
        ("Steve Jobs", "Walter Isaacson", 32.0),
        ("Grokking Algorithms", "Aditya Bhargava", 34.0),
        ("Fluent Python", "Luciano Ramalho", 46.0),
        ("Learning Python", "Mark Lutz", 52.0),
        ("Effective Python", "Brett Slatkin", 38.0),
        ("Programming Rust", "Jim Blandy", 49.0),
        ("The Go Programming Language", "Alan Donovan", 43.0),
        ("Eloquent JavaScript", "Marijn Haverbeke", 31.0),
        ("JavaScript: The Good Parts", "Douglas Crockford", 27.0),
        ("Working Effectively with Legacy Code", "Michael Feathers", 41.0),
        ("Patterns of Enterprise Application Architecture", "Martin Fowler", 58.0),
        ("Cracking the Coding Interview", "Gayle Laakmann McDowell", 36.0),
        ("The Mythical Man-Month", "Frederick Brooks", 29.0),
        ("Computer Systems: A Programmer's Perspective", "Randal Bryant", 75.0),
        ("Operating Systems: Three Easy Pieces", "Remzi Arpaci-Dusseau", 40.0),
        ("Computer Networking: A Top-Down Approach", "James Kurose", 85.0),
        ("Modern Operating Systems", "Andrew Tanenbaum", 95.0),
        ("Database System Concepts", "Abraham Silberschatz", 110.0),
        ("Compilers: Principles, Techniques, and Tools", "Alfred Aho", 120.0),
        ("The Art of Computer Programming", "Donald Knuth", 200.0),
        ("Soft Skills", "John Sonmez", 24.0),
        ("The Complete Software Developer's Career Guide", "John Sonmez", 33.0),
        ("The Clean Coder", "Robert C. Martin", 37.0),
        ("Pro Git", "Scott Chacon", 0.0),
        ("Docker Deep Dive", "Nigel Poulton", 39.0),
        ("Kubernetes Up & Running", "Brendan Burns", 41.0),
        ("Designing Data-Intensive Applications", "Martin Kleppmann", 54.0),
        ("Site Reliability Engineering", "Betsy Beyer", 42.0),
        ("The Phoenix Project", "Gene Kim", 21.0),
        ("The Unicorn Project", "Gene Kim", 23.0),
        ("Accelerate", "Nicole Forsgren", 25.0),
    ]
    
    for i, (title, author, price) in enumerate(base_books):
        Book.addBook(id=f"b{i+1}", title=title, author=author, price=price, stock_quantity=10 + i)
        
    # 3. Create Ratings (for recommendations)
    b1 = Book.objects.get(id="b1")
    b2 = Book.objects.get(id="b2")
    b7 = Book.objects.get(id="b7")
    
    Rating.objects.get_or_create(customer=c1, book=b1, defaults={"score": 5.0})
    Rating.objects.get_or_create(customer=c2, book=b1, defaults={"score": 4.5})
    Rating.objects.get_or_create(customer=c1, book=b2, defaults={"score": 4.8})
    # ...existing code...
    Rating.objects.get_or_create(customer=c2, book=b7, defaults={"score": 5.0})
    
    # 4. Create dummy orders/carts for "Customers also bought" logic
    from store.models.order.models import Cart, CartItem
    
    # Create a few carts where users bought related sets of books
    def add_related_purchase(customer, book_ids):
        cart = Cart.objects.create(customer=customer, is_active=False)
        for b_id in book_ids:
            try:
                book = Book.objects.get(id=b_id)
                CartItem.objects.create(cart=cart, book=book, quantity=1)
            except Book.DoesNotExist:
                pass

    # Group 1: People who like Clean Code also buy Clean Architecture and Refactoring
    add_related_purchase(c1, ["b1", "b9", "b14"])
    add_related_purchase(c2, ["b1", "b14", "b10"])
    
    # Group 2: People who like Atomic Habits also buy Psychology of Money
    add_related_purchase(c1, ["b7", "b8", "b18"])
    
    # Group 3: Python lovers
    add_related_purchase(c2, ["b4", "b22", "b23", "b24"])
    
    print("Done seeding!")

if __name__ == "__main__":
    seed_data()
