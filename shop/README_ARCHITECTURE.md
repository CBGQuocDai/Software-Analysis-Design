# Shop Project - Django Model-DAO-View-Template Architecture

## Overview

This is a complete Django project implementing a book shop system using the **Model-DAO-View-Template** architecture pattern. The project demonstrates proper separation of concerns and follows Django best practices.

## Architecture

### Layered Architecture

```
┌─────────────────────────────────────────┐
│           TEMPLATES (Presentation)       │
│   (books.html, cart.html, etc.)          │
└──────────────┬──────────────────────────┘
               │
┌──────────────▼──────────────────────────┐
│           VIEWS (Controller)             │
│   (views.py - Request Handling)          │
└──────────────┬──────────────────────────┘
               │
┌──────────────▼──────────────────────────┐
│           DAO (Data Access)              │
│  (book_dao.py, customer_dao.py, etc.)   │
└──────────────┬──────────────────────────┘
               │
┌──────────────▼──────────────────────────┐
│           MODELS (Data Layer)            │
│  (models/customer.py, models/book.py)   │
└──────────────┬──────────────────────────┘
               │
┌──────────────▼──────────────────────────┐
│           DATABASE (SQLite)              │
└──────────────────────────────────────────┘
```

## Project Structure

```
shop/
├── manage.py                          # Django management script
├── db.sqlite3                         # SQLite database
├── core/                              # Main application
│   ├── models/                        # Data models
│   │   ├── __init__.py
│   │   ├── customer.py               # Customer model
│   │   ├── book.py                   # Book model
│   │   ├── cart.py                   # Cart model
│   │   └── cart_item.py              # CartItem model
│   ├── dao/                           # Data Access Objects
│   │   ├── __init__.py
│   │   ├── book_dao.py               # Book data operations
│   │   ├── customer_dao.py           # Customer data operations
│   │   └── cart_dao.py               # Cart data operations
│   ├── templates/core/                # HTML templates
│   │   ├── books.html                # Book catalog page
│   │   ├── cart.html                 # Shopping cart page
│   │   ├── login.html                # Login page
│   │   └── register.html             # Registration page
│   ├── management/                    # Management commands
│   │   └── commands/
│   │       └── load_sample_data.py   # Load sample data
│   ├── migrations/                    # Database migrations
│   ├── views.py                       # View functions (controllers)
│   ├── urls.py                        # URL routing for core app
│   ├── apps.py                        # App configuration
│   └── admin.py                       # Django admin setup
└── shop/                              # Project configuration
    ├── settings.py                    # Django settings
    ├── urls.py                        # Main URL configuration
    ├── wsgi.py                        # WSGI configuration
    └── asgi.py                        # ASGI configuration
```

## Entities (Models)

### 1. Customer
- **id**: Integer (PK)
- **name**: String
- **email**: String (Unique)
- **password**: String (Hashed)
- **created_at**: DateTime

### 2. Book
- **id**: Integer (PK)
- **title**: String
- **author**: String
- **price**: Decimal (10.2)
- **stock**: Integer
- **created_at**: DateTime
- **updated_at**: DateTime

### 3. Cart
- **id**: Integer (PK)
- **customer_id**: FK → Customer (OneToOne)
- **created_at**: DateTime
- **updated_at**: DateTime

### 4. CartItem
- **id**: Integer (PK)
- **cart_id**: FK → Cart (Many-to-One)
- **book_id**: FK → Book (Many-to-One)
- **quantity**: Integer (≥ 1)
- **added_at**: DateTime

## DAO Layer

The DAO (Data Access Object) layer provides a clean interface to the database. All database queries go through DAOs, ensuring:
- Separation from Views
- Reusability
- Testability
- Maintainability

### BookDAO
**Static Methods:**
- `get_all_books()` - Get all books
- `get_book_by_id(id)` - Get book by ID
- `create_book(title, author, price, stock)` - Create new book
- `update_stock(book_id, quantity)` - Update stock

### CustomerDAO
**Static Methods:**
- `create_customer(name, email, password)` - Create new customer
- `get_customer_by_id(id)` - Get customer by ID
- `get_customer_by_email(email)` - Get customer by email
- `authenticate_customer(email, password)` - Authenticate login

### CartDAO
**Static Methods:**
- `get_or_create_cart(customer)` - Get or create cart
- `add_to_cart(customer, book_id, quantity=1)` - Add item to cart
- `get_cart_items(customer)` - Get all cart items
- `remove_item(cart_item_id)` - Remove item from cart
- `update_cart_item_quantity(cart_item_id, quantity)` - Update quantity
- `get_cart_total(customer)` - Calculate cart total
- `clear_cart(customer)` - Clear all items

## Views (Controllers)

### Authentication Routes
- **register(request)** - Customer registration
- **login(request)** - Customer login
- **logout(request)** - Customer logout

### Book Routes
- **book_list(request)** - Display all books

### Cart Routes
- **cart_view(request, customer_id)** - Display shopping cart
- **add_to_cart(request, customer_id, book_id)** - Add book to cart
- **remove_from_cart(request, customer_id, cart_item_id)** - Remove item
- **update_cart_item(request, customer_id, cart_item_id)** - Update quantity

## URL Routes

```
/register/                              - Register new customer
/login/                                 - Login page
/logout/                                - Logout
/books/                                 - View all books
/cart/<customer_id>/                    - View shopping cart
/cart/add/<customer_id>/<book_id>/      - Add book to cart
/cart/remove/<customer_id>/<cart_item_id>/ - Remove from cart
/cart/update/<customer_id>/<cart_item_id>/ - Update cart item quantity
```

## Installation & Setup

### 1. Install Dependencies
```bash
pip install django
```

### 2. Run Migrations
```bash
python manage.py migrate
```

### 3. Load Sample Data
```bash
python manage.py load_sample_data
```

### 4. Create Admin User (Optional)
```bash
python manage.py createsuperuser
```

### 5. Start Development Server
```bash
python manage.py runserver
```

The application will be available at: `http://localhost:8000/books/`

## Key Features

### ✓ Proper Layering
- No ORM queries in Views
- All database access through DAO
- Views only orchestrate and handle HTTP

### ✓ Authentication
- User registration with password hashing
- Secure login with session management
- Session-based authorization

### ✓ Shopping Cart
- Add/remove books dynamically
- Update quantities
- Calculate total price
- Session-based storage

### ✓ Responsive UI
- Clean, modern design
- Mobile-friendly templates
- Form validation and error handling

## Code Quality Standards

### Architecture Rules
1. ✓ No direct ORM calls in Views (`Book.objects.all()` NOT in views.py)
2. ✓ All queries go through DAO layer
3. ✓ DAOs only interact with Models
4. ✓ No business logic in Templates
5. ✓ Views are thin controllers

### Security Measures
- Password hashing using Django's hashers
- CSRF token protection in forms
- Session-based authentication
- Input validation

## Sample Data

The system includes 6 sample books:
1. Python Pro - 150,000 ₫ (10 in stock)
2. Django Mastery - 180,000 ₫ (8 in stock)
3. Web Development Basics - 120,000 ₫ (15 in stock)
4. Database Design - 160,000 ₫ (12 in stock)
5. REST API Guide - 140,000 ₫ (20 in stock)
6. Vue.js Complete Guide - 175,000 ₫ (9 in stock)

## Testing the Application

### Test Registration
1. Go to `/register/`
2. Fill in name, email, and password
3. Submit
4. Should redirect to login

### Test Login
1. Go to `/login/`
2. Enter registered email and password
3. Should redirect to book list

### Test Shopping
1. View books at `/books/`
2. Click "Thêm vào giỏ" (Add to cart)
3. View cart at `/cart/<customer_id>/`
4. Can update quantities or remove items

## Development Tips

### To Add a New Feature
1. Update models if needed in `core/models/`
2. Add DAO methods in appropriate `core/dao/` file
3. Add View functions in `core/views.py`
4. Add URL routes in `core/urls.py`
5. Create/update templates in `core/templates/core/`
6. Run migrations if models changed

### To Debug
- Check database queries through Django ORM
- Use Django admin at `/admin/`
- Check console output for errors
- Use browser developer tools

## Production Considerations

For production deployment:
1. Set `DEBUG = False` in settings.py
2. Update `ALLOWED_HOSTS` with domain
3. Use PostgreSQL instead of SQLite
4. Set secure password hashing algorithm
5. Use environment variables for secrets
6. Enable HTTPS
7. Use proper WSGI server (Gunicorn, etc.)

## License

Educational project for learning Django architecture patterns.

## Author

Created as a demonstration of Django best practices and clean architecture.
