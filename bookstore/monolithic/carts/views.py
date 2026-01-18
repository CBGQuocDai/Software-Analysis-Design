from django.shortcuts import render, redirect
from books.models import Book
from .models import Cart, CartItem
from common.utils import get_current_customer


def add_to_cart(request, book_id):
    customer = get_current_customer(request)
    if not customer:
        return redirect('login')
    book = Book.objects.get(id=book_id)

    if request.method == "POST":
        quantity = int(request.POST.get('quantity', 1))

        cart, _ = Cart.objects.get_or_create(customer=customer)

        item, created = CartItem.objects.get_or_create(
            cart=cart,
            book=book
        )

        if not created:
            item.quantity += quantity
        else:
            item.quantity = quantity

        item.save()

        return redirect('book_list')

def view_cart(request):
    customer = get_current_customer(request)

    if not customer:
        return redirect('login')
    
    cart = Cart.objects.filter(customer=customer).first()
    items = cart.items.all() if cart else []
    total = 0
    for item in items:
        total += item.book.price * item.quantity

    context = {
        'items': items,
        'total': total
    }

    return render(request, 'carts/cart.html', context)
