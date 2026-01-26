from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse

from store.models import Book, Cart, CartItem, Customer, Order


def _get_guest_customer() -> Customer:
    customer, _ = Customer.objects.get_or_create(
        id="guest",
        defaults={"name": "Guest", "email": "guest@example.com", "password": "guest"},
    )
    return customer


def _get_active_cart(customer: Customer) -> Cart:
    cart, _ = Cart.objects.get_or_create(customer=customer, is_active=True)
    return cart


def cart_view(request: HttpRequest) -> HttpResponse:
    customer = _get_guest_customer()
    cart = _get_active_cart(customer)
    items = cart.items.select_related("book").all()

    total = 0.0
    for item in items:
        total += float(item.book.price) * int(item.quantity)

    return render(request, "cart/view.html", {"cart": cart, "items": items, "total": total})


def add_to_cart(request: HttpRequest, book_id: str) -> HttpResponse:
    customer = _get_guest_customer()
    cart = _get_active_cart(customer)
    book = Book.objects.get(id=book_id)
    CartItem.addItem(cart=cart, book=book, quantity=1)
    return redirect(reverse("cart_view"))


def create_order(request: HttpRequest) -> HttpResponse:
    customer = _get_guest_customer()
    cart = _get_active_cart(customer)
    items = list(cart.items.select_related("book").all())

    if request.method == "POST":
        payment_method = request.POST.get("payment_method", "COD")
        shipping_method = request.POST.get("shipping_method", "Standard")
        
        total = 0.0
        for item in items:
            total += float(item.book.price) * int(item.quantity)
            
        # Add shipping fee
        shipping_fee = 0.0
        if shipping_method == "Express":
            shipping_fee = 5.0
        elif shipping_method == "Next Day":
            shipping_fee = 15.0
        
        final_total = total + shipping_fee

        order = Order.createOrder(customer=customer, total_price=final_total)
        
        # Create Payment and Shipping records
        from store.models.order.models import Payment, Shipping
        Payment.objects.create(order=order, method_name=payment_method, status="Paid" if payment_method != "COD" else "Pending")
        Shipping.objects.create(order=order, method_name=shipping_method, fee=shipping_fee)

        cart.is_active = False
        cart.save(update_fields=["is_active"])

        return render(request, "cart/order_created.html", {
            "order": order, 
            "total": final_total,
            "payment_method": payment_method,
            "shipping_method": shipping_method
        })
    
    return redirect(reverse("cart_view"))


def order_history(request: HttpRequest) -> HttpResponse:
    customer = _get_guest_customer()
    orders = Order.objects.filter(customer=customer).order_by("-created_at")
    
    # Pre-fetch payment and shippings for efficiency if needed
    # But usually OneToOne and ForeignKey can be accessed directly in templates
    
    return render(request, "cart/order_history.html", {"orders": orders})
