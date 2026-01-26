from django.db import models


class Book(models.Model):
    id = models.CharField(max_length=64, primary_key=True)
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    price = models.FloatField()
    stock_quantity = models.IntegerField(default=0)

    def __str__(self) -> str:
        return f"{self.title} ({self.id})"

    @classmethod
    def addBook(cls, *, id: str, title: str, author: str, price: float, stock_quantity: int = 0) -> "Book":
        book, _created = cls.objects.update_or_create(
            id=id,
            defaults={
                "title": title,
                "author": author,
                "price": price,
                "stock_quantity": stock_quantity,
            },
        )
        return book

    @classmethod
    def searchBook(cls, *, query: str) -> models.QuerySet["Book"]:
        return cls.objects.filter(models.Q(title__icontains=query) | models.Q(author__icontains=query))


class Rating(models.Model):
    customer = models.ForeignKey("store.Customer", on_delete=models.CASCADE, related_name="ratings")
    book = models.ForeignKey("store.Book", on_delete=models.CASCADE, related_name="ratings")
    score = models.FloatField()

    class Meta:
        unique_together = ("customer", "book")

    def __str__(self) -> str:
        return f"{self.customer_id} -> {self.book_id}: {self.score}"
