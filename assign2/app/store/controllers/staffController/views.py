from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from store.models import Staff


def staff_list(request: HttpRequest) -> HttpResponse:
    staff_members = Staff.objects.all().order_by("name")
    return render(request, "staff/list.html", {"staff": staff_members})
