from django.urls import path

from store.controllers.orderController.views import add_to_cart, cart_view, create_order, order_history

urlpatterns = [
    path("cart/", cart_view, name="cart_view"),
    path("cart/add/<str:book_id>/", add_to_cart, name="cart_add"),
    path("order/create/", create_order, name="order_create"),
    path("order/history/", order_history, name="order_history"),
]
