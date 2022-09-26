from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class Account(AbstractUser):
    
    gender_list = [
        ('Male','Male'),
        ('Female','Female'),
    ]

    email = models.CharField(max_length=120,unique=True)
    username = models.CharField(max_length=120,unique=True)
    contact_number = models.CharField(max_length=20,null=True,blank=True)
    dob = models.DateField(null=True,blank=True)
    gender = models.CharField(choices=gender_list,max_length=10,null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at =models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.username


class Address(models.Model):
    user = models.ForeignKey(Account,on_delete=models.CASCADE, null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    pincode = models.CharField(max_length=50, null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)
    state = models.CharField(max_length=100, null=True, blank=True)
    country = models.CharField(max_length=100, null=True, blank=True)   
    
    
class Contact(models.Model):
    email = models.CharField(max_length=255)