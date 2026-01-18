from django.urls import path
from .views import *

urlpatterns = [
    path('accounts/register/', register_view),
    path('accounts/login/', login_view),
    path('', catalog_view),
    path('cart/', cart_view),
    path('cart/add/<int:book_id>/', add_to_cart_view),
]
