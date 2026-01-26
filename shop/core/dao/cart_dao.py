from core.models.cart import Cart
from core.models.cart_item import CartItem
from core.models.book import Book


class CartDAO:
    """Data Access Object for Cart model - handles all cart-related database operations"""

    @staticmethod
    def get_or_create_cart(customer):
        """
        Get or create a cart for a customer
        
        Args:
            customer (Customer): The customer object
            
        Returns:
            Cart: The customer's cart (existing or newly created)
        """
        cart, created = Cart.objects.get_or_create(customer=customer)
        return cart

    @staticmethod
    def add_to_cart(customer, book_id, quantity=1):
        """
        Add a book to a customer's cart or update quantity if already exists
        
        Args:
            customer (Customer): The customer object
            book_id (int): The ID of the book to add
            quantity (int): The quantity to add (default: 1)
            
        Returns:
            CartItem: The created or updated CartItem object, or None if book not found
        """
        # Get or create cart
        cart = CartDAO.get_or_create_cart(customer)
        
        # Verify book exists
        try:
            book = Book.objects.get(id=book_id)
        except Book.DoesNotExist:
            return None
        
        # Check if item already exists in cart
        try:
            cart_item = CartItem.objects.get(cart=cart, book=book)
            # Update quantity
            cart_item.quantity += quantity
            cart_item.save()
        except CartItem.DoesNotExist:
            # Create new cart item
            cart_item = CartItem(cart=cart, book=book, quantity=quantity)
            cart_item.save()
        
        return cart_item

    @staticmethod
    def get_cart_items(customer):
        """
        Get all items in a customer's cart
        
        Args:
            customer (Customer): The customer object
            
        Returns:
            QuerySet: All CartItem objects for this customer, or empty QuerySet if no cart
        """
        try:
            cart = Cart.objects.get(customer=customer)
            return cart.items.all()
        except Cart.DoesNotExist:
            return CartItem.objects.none()

    @staticmethod
    def remove_item(cart_item_id):
        """
        Remove an item from a cart
        
        Args:
            cart_item_id (int): The ID of the cart item to remove
            
        Returns:
            bool: True if item was deleted, False if not found
        """
        try:
            cart_item = CartItem.objects.get(id=cart_item_id)
            cart_item.delete()
            return True
        except CartItem.DoesNotExist:
            return False

    @staticmethod
    def update_cart_item_quantity(cart_item_id, quantity):
        """
        Update the quantity of an item in the cart
        
        Args:
            cart_item_id (int): The ID of the cart item
            quantity (int): The new quantity (must be >= 1)
            
        Returns:
            CartItem: The updated CartItem object or None if not found
        """
        try:
            cart_item = CartItem.objects.get(id=cart_item_id)
            if quantity < 1:
                cart_item.delete()
                return None
            cart_item.quantity = quantity
            cart_item.save()
            return cart_item
        except CartItem.DoesNotExist:
            return None

    @staticmethod
    def get_cart_total(customer):
        """
        Calculate the total price of all items in a customer's cart
        
        Args:
            customer (Customer): The customer object
            
        Returns:
            float: Total price of all items in the cart
        """
        cart_items = CartDAO.get_cart_items(customer)
        total = 0
        for item in cart_items:
            total += item.book.price * item.quantity
        return total

    @staticmethod
    def clear_cart(customer):
        """
        Clear all items from a customer's cart
        
        Args:
            customer (Customer): The customer object
        """
        try:
            cart = Cart.objects.get(customer=customer)
            cart.items.all().delete()
        except Cart.DoesNotExist:
            pass
