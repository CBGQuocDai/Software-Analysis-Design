from django.contrib import admin

from .models import Book, Cart, CartItem, Customer, Order, Payment, Rating, Shipping, Staff

admin.site.register(Book)
admin.site.register(Rating)
admin.site.register(Customer)
admin.site.register(Staff)
admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(Order)
admin.site.register(Payment)
admin.site.register(Shipping)
