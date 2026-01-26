from django.shortcuts import render, redirect
from django.http import JsonResponse
from core.dao.book_dao import BookDAO
from core.dao.customer_dao import CustomerDAO
from core.dao.cart_dao import CartDAO
from core.models.customer import Customer


def register(request):
    """
    Handle customer registration
    GET: Display registration form
    POST: Create new customer account
    """
    if request.method == 'POST':
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        password = request.POST.get('password', '')
        
        if not all([name, email, password]):
            return render(request, 'core/register.html', {
                'error': 'Tất cả các trường là bắt buộc'
            })
        
        # Use CustomerDAO to create customer
        customer = CustomerDAO.create_customer(name, email, password)
        
        if customer:
            # Redirect to login page with success message
            return redirect('core:login')
        else:
            return render(request, 'core/register.html', {
                'error': 'Email đã được sử dụng'
            })
    
    return render(request, 'core/register.html')


def login(request):
    """
    Handle customer login
    GET: Display login form
    POST: Authenticate customer and create session
    """
    if request.method == 'POST':
        email = request.POST.get('email', '')
        password = request.POST.get('password', '')
        
        if not all([email, password]):
            return render(request, 'core/login.html', {
                'error': 'Email và mật khẩu là bắt buộc'
            })
        
        # Use CustomerDAO to authenticate
        customer = CustomerDAO.authenticate_customer(email, password)
        
        if customer:
            # Store customer ID in session
            request.session['customer_id'] = customer.id
            return redirect('core:book_list')
        else:
            return render(request, 'core/login.html', {
                'error': 'Email hoặc mật khẩu không chính xác'
            })
    
    return render(request, 'core/login.html')


def logout(request):
    """Handle customer logout"""
    if 'customer_id' in request.session:
        del request.session['customer_id']
    return redirect('core:book_list')


def book_list(request):
    """
    Display all books in the catalog
    Uses BookDAO to retrieve books from database
    """
    # Use BookDAO to get all books
    books = BookDAO.get_all_books()
    
    context = {
        'books': books,
        'is_logged_in': 'customer_id' in request.session
    }
    
    if 'customer_id' in request.session:
        # Use CustomerDAO to get customer
        customer = CustomerDAO.get_customer_by_id(request.session['customer_id'])
        if customer:
            context['customer'] = customer
        else:
            del request.session['customer_id']
    
    return render(request, 'core/books.html', context)


def add_to_cart(request, customer_id, book_id):
    """
    Add a book to customer's cart
    GET: Returns JSON response
    Redirects to cart view
    
    Args:
        customer_id (int): The customer's ID
        book_id (int): The book's ID
    """
    # Verify customer is logged in and owns this cart
    if 'customer_id' not in request.session or request.session['customer_id'] != customer_id:
        return redirect('core:login')
    
    # Use CustomerDAO to verify customer exists
    customer = CustomerDAO.get_customer_by_id(customer_id)
    if not customer:
        return redirect('core:login')
    
    # Use CartDAO to add item to cart
    cart_item = CartDAO.add_to_cart(customer, book_id, quantity=1)
    
    if cart_item is None:
        return redirect('core:book_list')
    
    # Redirect to cart view
    return redirect('core:cart_view', customer_id=customer_id)


def cart_view(request, customer_id):
    """
    Display customer's shopping cart
    Shows all items in the cart with quantities and prices
    
    Args:
        customer_id (int): The customer's ID
    """
    # Verify customer is logged in and owns this cart
    if 'customer_id' not in request.session or request.session['customer_id'] != customer_id:
        return redirect('core:login')
    
    # Use CustomerDAO to get customer
    customer = CustomerDAO.get_customer_by_id(customer_id)
    if not customer:
        return redirect('core:login')
    
    # Use CartDAO to get cart items
    cart_items = CartDAO.get_cart_items(customer)
    total_price = CartDAO.get_cart_total(customer)
    
    context = {
        'cart_items': cart_items,
        'customer': customer,
        'total_price': total_price,
        'is_logged_in': True
    }
    
    return render(request, 'core/cart.html', context)


def remove_from_cart(request, customer_id, cart_item_id):
    """
    Remove an item from customer's cart
    
    Args:
        customer_id (int): The customer's ID
        cart_item_id (int): The cart item's ID
    """
    # Verify customer is logged in and owns this cart
    if 'customer_id' not in request.session or request.session['customer_id'] != customer_id:
        return redirect('core:login')
    
    # Use CartDAO to remove item
    CartDAO.remove_item(cart_item_id)
    
    # Redirect back to cart view
    return redirect('core:cart_view', customer_id=customer_id)


def update_cart_item(request, customer_id, cart_item_id):
    """
    Update quantity of an item in the cart
    
    Args:
        customer_id (int): The customer's ID
        cart_item_id (int): The cart item's ID
    """
    # Verify customer is logged in and owns this cart
    if 'customer_id' not in request.session or request.session['customer_id'] != customer_id:
        return redirect('core:login')
    
    if request.method == 'POST':
        quantity = int(request.POST.get('quantity', 1))
        
        # Use CartDAO to update quantity
        CartDAO.update_cart_item_quantity(cart_item_id, quantity)
    
    # Redirect back to cart view
    return redirect('core:cart_view', customer_id=customer_id)
