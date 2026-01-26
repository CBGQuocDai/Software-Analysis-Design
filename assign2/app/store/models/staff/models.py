from django.db import models


class Staff(models.Model):
    id = models.CharField(max_length=64, primary_key=True)
    name = models.CharField(max_length=255)
    role = models.CharField(max_length=100)

    def __str__(self) -> str:
        return f"{self.name} ({self.role})"
