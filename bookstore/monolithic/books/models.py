from django.db import models

class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    stock = models.IntegerField()
    price = models.IntegerField()  # Price in VND

    def __str__(self):
        return self.title
