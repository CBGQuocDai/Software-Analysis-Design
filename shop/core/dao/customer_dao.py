from django.contrib.auth.hashers import make_password
from core.models.customer import Customer


class CustomerDAO:
    """Data Access Object for Customer model - handles all customer-related database operations"""

    @staticmethod
    def create_customer(name, email, password):
        """
        Create a new customer in the database
        
        Args:
            name (str): Customer name
            email (str): Customer email (must be unique)
            password (str): Customer password
            
        Returns:
            Customer: The newly created Customer object or None if email already exists
        """
        # Check if customer with this email already exists
        if Customer.objects.filter(email=email).exists():
            return None
        
        # Hash the password for security
        hashed_password = make_password(password)
        customer = Customer(name=name, email=email, password=hashed_password)
        customer.save()
        return customer

    @staticmethod
    def get_customer_by_id(customer_id):
        """
        Retrieve a customer by ID
        
        Args:
            customer_id (int): The ID of the customer
            
        Returns:
            Customer: The Customer object or None if not found
        """
        try:
            return Customer.objects.get(id=customer_id)
        except Customer.DoesNotExist:
            return None

    @staticmethod
    def get_customer_by_email(email):
        """
        Retrieve a customer by email
        
        Args:
            email (str): The email of the customer
            
        Returns:
            Customer: The Customer object or None if not found
        """
        try:
            return Customer.objects.get(email=email)
        except Customer.DoesNotExist:
            return None

    @staticmethod
    def authenticate_customer(email, password):
        """
        Authenticate a customer by email and password
        
        Args:
            email (str): Customer email
            password (str): Customer password (plain text)
            
        Returns:
            Customer: The Customer object if credentials are valid, None otherwise
        """
        customer = CustomerDAO.get_customer_by_email(email)
        if customer:
            # Import here to avoid circular imports
            from django.contrib.auth.hashers import check_password
            if check_password(password, customer.password):
                return customer
        return None

    @staticmethod
    def customer_exists(customer_id):
        """
        Check if a customer exists by ID
        
        Args:
            customer_id (int): The customer ID
            
        Returns:
            bool: True if customer exists, False otherwise
        """
        return Customer.objects.filter(id=customer_id).exists()
