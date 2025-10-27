from django.db import models
from taggit.managers import TaggableManager


class Type(models.TextChoices):
    FERTILIZER = 'Fertilizer', 'کود'
    POISON = 'Poison', 'سم'
    COMBINED = 'Combined', 'ترکیبی'

class Product(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100)
    weight = models.DecimalField(max_digits=5, decimal_places=2)
    type = models.CharField(max_length=10, choices=Type.choices)
    SKU = models.CharField(max_length=50)
    brand = models.CharField(max_length=50)
    description = models.TextField()
    price = models.DecimalField(max_digits=5, decimal_places=2)
    production_date = models.DateField()
    expiration_date = models.DateField()
    tags = TaggableManager()
    is_active = models.BooleanField(default=True)
    updated_at = models.DateTimeField(auto_now=True)


