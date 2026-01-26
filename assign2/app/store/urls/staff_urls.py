from django.urls import path

from store.controllers.staffController.views import staff_list

urlpatterns = [
    path("staff/", staff_list, name="staff_list"),
]
