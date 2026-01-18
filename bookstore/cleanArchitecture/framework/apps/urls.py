from django.urls import path
from .views import *

urlpatterns = [
    path('accounts/register/', register_view, name='register'),
    path('accounts/login/', login_view, name='login'),
    path('', catalog_view, name='catalog'),
    path('cart/', cart_view, name='cart'),
    path('cart/add/<int:book_id>/', add_to_cart_view, name='add_cart'),
]
