from django.db import models


# Create your models here.

class Product(models.Model):  # this line defines our model (it is an object)
    title = models.CharField(max_length=120)
    description = models.TextField(blank=True, null=True)  # if do not want text then blank=True null=True
    price = models.DecimalField(default=0.00, decimal_places=2, max_digits=10)
    summary = models.TextField(blank=False, null=False)
    featured = models.BooleanField(default=False)
