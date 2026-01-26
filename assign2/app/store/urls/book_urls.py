from django.urls import path

from store.controllers.bookController.views import book_detail, book_list

urlpatterns = [
    path("", book_list, name="home"),
    path("books/", book_list, name="book_list"),
    path("books/<str:book_id>/", book_detail, name="book_detail"),
]
