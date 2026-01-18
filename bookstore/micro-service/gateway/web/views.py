from django.shortcuts import render, redirect
from .clients.customer import CustomerClient
from .clients.book import BookClient
from .clients.cart import CartClient

from .forms import RegisterForm, LoginForm, AddToCartForm
from .utils import get_current_user
# auth
def register_view(request):
    form = RegisterForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        result = CustomerClient.register(form.cleaned_data)
        if "id" in result:
            return redirect("/accounts/login/")
        return render(request, "register.html", {
            "form": form,
            "error": result
        })
    return render(request, "register.html", {"form": form})
def login_view(request):
    form = LoginForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        result = CustomerClient.login(form.cleaned_data)

        if "id" in result:
            request.session["customer_id"] = result["id"]
            return redirect("/")

        return render(request, "login.html", {
            "form": form,
            "error": result
        })
    return render(request, "login.html", {"form": form})
# book
def catalog_view(request):
    books = BookClient.list_books()
    return render(request, "list.html", {
        "books": books
    })
# cart
def add_to_cart_view(request, book_id):
    user = get_current_user(request)
    if not user:
        return redirect("/accounts/login/")
    form = AddToCartForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        data = {
            "customer_id": user["id"],
            "book_id": book_id,
            "quantity": form.cleaned_data["quantity"]
        }
        CartClient.add_to_cart(data)
    return redirect("/")
def cart_view(request):
    user = get_current_user(request)
    if not user:
        return redirect("/accounts/login/")
    cart = CartClient.get_cart(user["id"])
    items = []
    for item in cart.get("items", []):
        book = item["book"]
        items.append({
            "book": book,
            "quantity": item["quantity"],
        })
    total_price = sum(item["book"]["price"] * item["quantity"] for item in items)
    return render(request, "cart.html", {
        "items": items,
        "total": total_price
    })

