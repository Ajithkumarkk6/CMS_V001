from django.db import models

# Create your models here.
from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    # Add any other fields specific to your product

    def __str__(self):
        return self.name


class Size(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='sizes')
    name = models.CharField(max_length=50)
    quantity = models.PositiveIntegerField()
    length = models.DecimalField(max_digits=10, decimal_places=2)
    breadth = models.DecimalField(max_digits=10, decimal_places=2)
    # Add any other fields specific to the size (e.g., weight, height, etc.)

    def __str__(self):
        return f"{self.name} ({self.product.name})"
