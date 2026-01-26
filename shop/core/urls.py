from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    # Authentication routes
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    
    # Book routes
    path('books/', views.book_list, name='book_list'),
    
    # Cart routes
    path('cart/<int:customer_id>/', views.cart_view, name='cart_view'),
    path('cart/add/<int:customer_id>/<int:book_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/remove/<int:customer_id>/<int:cart_item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('cart/update/<int:customer_id>/<int:cart_item_id>/', views.update_cart_item, name='update_cart_item'),
]
