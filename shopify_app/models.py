from django.db import models

# Create your models here.
class Shop(models.Model):
    name = models.CharField(max_length=255)
    installed = models.BooleanField(default=True)
    created_on = models.DateTimeField(auto_now_add=True)