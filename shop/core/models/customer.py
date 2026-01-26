from django.db import models


class Customer(models.Model):
    """Customer model representing a registered user in the system"""
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        app_label = 'core'
        db_table = 'core_customer'

    def __str__(self):
        return f"{self.name} ({self.email})"
