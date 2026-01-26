from django.urls import path

from store.controllers.customerController.views import customer_list

urlpatterns = [
    path("customers/", customer_list, name="customer_list"),
]
