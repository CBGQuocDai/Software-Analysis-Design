from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from store.models import Customer


def customer_list(request: HttpRequest) -> HttpResponse:
    customers = Customer.objects.all().order_by("name")
    return render(request, "staff/customers.html", {"customers": customers})
