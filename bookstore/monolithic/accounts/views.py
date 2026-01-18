from django.shortcuts import render, redirect
from .forms import RegisterForm, LoginForm
from .models import Customer


def register_view(request):
    form = RegisterForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect('login')

    return render(request, 'accounts/register.html', {'form': form})
def login_view(request):
    form = LoginForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        email = form.cleaned_data['email']
        password = form.cleaned_data['password']

        try:
            user = Customer.objects.get(email=email, password=password)

            # Lưu vào session
            request.session['customer_id'] = user.id

            return redirect('book_list')

        except Customer.DoesNotExist:
            form.add_error(None, "Invalid credentials")

    return render(request, 'accounts/login.html', {'form': form})
