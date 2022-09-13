from django.db import models

# Create your models here.

class contact(models.Model):
    name = models.CharField(max_length=20)
    email = models.CharField(max_length=20)
    phone = models.CharField(max_length=15)
    subject = models.CharField(max_length=20)
    message = models.CharField(max_length=200)
    
    def __str__(self):
        return self.name
