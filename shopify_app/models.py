from django.db import models

# Create your models here.
class Shop(models.Model):
    name = models.CharField(max_length=255)
    installed = models.BooleanField(default=True)
    created_on = models.DateTimeField(auto_now_add=True)

class Task(models.Model):
    method = models.CharField(max_length=255)
    data = models.TextField(default='{}')
    retry = models.IntegerField(default = 3)
    executed = models.BooleanField(default = False)
    scheduled_on = models.DateTimeField(auto_now_add=True)
    created_on = models.DateTimeField(auto_now_add=True)
