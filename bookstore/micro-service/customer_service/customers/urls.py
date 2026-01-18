from django.urls import path
from .views import register, login, customer_detail

urlpatterns = [
    path('register/', register),
    path('login/', login),
    path('<int:customer_id>/', customer_detail),
]
