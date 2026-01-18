from django.urls import path
from .views import BookListAPI, BookDetailAPI

urlpatterns = [
    path('', BookListAPI.as_view()),
    path('<int:book_id>/', BookDetailAPI.as_view()),
]
