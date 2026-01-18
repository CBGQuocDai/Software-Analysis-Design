from django.urls import path
from .views import RegisterAPI, LoginAPI, CustomerDetailAPI

urlpatterns = [
    path('register/', RegisterAPI.as_view()),
    path('login/', LoginAPI.as_view()),
    path('<int:customer_id>/', CustomerDetailAPI.as_view()),
]
