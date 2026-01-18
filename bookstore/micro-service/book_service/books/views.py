from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import Book
from .serializers import BookSerializer


# API 1: GET /api/books/
class BookListAPI(APIView):

    def get(self, request):
        books = Book.objects.all()

        serializer = BookSerializer(books, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

# API 2: GET /api/books/<id>/
class BookDetailAPI(APIView):

    def get(self, request, book_id):
        try:
            book = Book.objects.get(id=book_id)
        except Book.DoesNotExist:
            return Response(
                {"error": "Book not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = BookSerializer(book)
        return Response(serializer.data, status=status.HTTP_200_OK)
