from django.shortcuts import render, redirect
from django.contrib import messages

# Forms từ layer interfaces
from interfaces.forms.auth_forms import RegisterForm, LoginForm
from interfaces.forms.cart_forms import AddToCartForm

# Controllers (kết nối tới Use Cases)
from interfaces.controllers import (
    register,
    login,
    list_books,
    add_to_cart,
    view_cart
)

# customer_view
def register_view(request):
    form = RegisterForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        try:
            register(form.cleaned_data)
            messages.success(request, "Đăng ký tài khoản thành công!")
            return redirect('login')
        except Exception as e:
            messages.error(request, str(e))

    return render(request, './accounts/register.html', {
        'form': form
    })


def login_view(request):
    form = LoginForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        user = login(form.cleaned_data)

        if user:
            request.session['customer_id'] = user.id
            messages.success(request, "Đăng nhập thành công!")
            return redirect('catalog')
        else:
            messages.error(request, "Email hoặc mật khẩu không đúng")

    return render(request, './accounts/login.html', {
        'form': form
    })


# book view
def catalog_view(request):
    books = list_books()

    return render(request, './books/list.html', {
        'books': books
    })

# cart view
def add_to_cart_view(request, book_id):
    if 'customer_id' not in request.session:
        return redirect('login')

    if request.method != "POST":
        return redirect('catalog')

    form = AddToCartForm(request.POST)

    if not form.is_valid():
        messages.error(request, "Số lượng không hợp lệ")
        return redirect('catalog')

    quantity = form.cleaned_data.get('quantity', 1)

    add_to_cart(
        request.session['customer_id'],
        book_id,
        quantity
    )

    messages.success(request, "Đã thêm vào giỏ hàng")
    return redirect('catalog')



def cart_view(request):
    # Kiểm tra đăng nhập
    if 'customer_id' not in request.session:
        return redirect('login')

    items = view_cart(request.session['customer_id'])
    # Tính tổng tiền theo đúng template hiện tại
    total = sum(item.book.price * item.quantity for item in items)

    return render(request, './carts/cart.html', {
        'items': items,
        'total': total
    })
