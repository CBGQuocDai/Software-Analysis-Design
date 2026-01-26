from django.http import Http404, HttpRequest, HttpResponse
from django.shortcuts import render
from django.db import models

from store.models import Book, CartItem


def recommend_books(book_id: str) -> list[Book]:
    """Gợi ý sách: Những người đã mua sách này cũng mua..."""
    related = CartItem.objects.filter(book_id=book_id)
    carts = [c.cart_id for c in related]
    items = CartItem.objects.filter(cart_id__in=carts)
    # Ưu tiên gợi ý các sách được đánh giá cao từ khách hàng có hành vi tương tự
    books = Book.objects.filter(id__in=[i.book_id for i in items]).annotate(
        avg_rating=models.Avg('ratings__score')
    ).order_by('-avg_rating', 'title')
    
    return list(books.exclude(id=book_id).distinct()[:4])


def book_list(request: HttpRequest) -> HttpResponse:
    query = request.GET.get("q", "").strip()
    if query:
        books = Book.searchBook(query=query)
    else:
        books = Book.objects.all().order_by("title")
    
    # Simple recommendation based on top ratings
    recommendations = Book.objects.annotate(
        avg_score=models.Avg('ratings__score')
    ).filter(avg_score__gte=4).order_by('-avg_score')[:4]
    
    return render(request, "book/list.html", {
        "books": books, 
        "query": query,
        "recommendations": recommendations
    })


def book_detail(request: HttpRequest, book_id: str) -> HttpResponse:
    try:
        book = Book.objects.get(id=book_id)
    except Book.DoesNotExist as exc:
        raise Http404("Book not found") from exc
    
    # Lấy danh sách gợi ý "People also bought"
    related_books = recommend_books(book_id)
    
    return render(request, "book/detail.html", {
        "book": book,
        "related_books": related_books
    })
