from django.urls import path
from .views import AddToCartAPI, GetCartAPI

urlpatterns = [
    path('add/', AddToCartAPI.as_view()),
    path('<int:customer_id>/', GetCartAPI.as_view()),
]
