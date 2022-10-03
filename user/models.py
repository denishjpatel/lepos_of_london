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
    user = models.ForeignKey(Account,on_delete=models.CASCADE, null=True, blank=True, unique=True)
    address = models.TextField(null=True, blank=True)
    pincode = models.CharField(max_length=50, null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)
    state = models.CharField(max_length=100, null=True, blank=True)
    country = models.CharField(max_length=100, null=True, blank=True)   
    
    
class Contact(models.Model):
    email = models.CharField(max_length=255)
    
    
class terms_conditions(models.Model):
    title = models.CharField(max_length = 50)
    sub_title = models.CharField(max_length = 50)
    text1 = models.CharField(max_length = 50)
    text2 = models.CharField(max_length = 50)
    text3 = models.CharField(max_length = 50)
    text4 = models.CharField(max_length = 50)
    text5 = models.CharField(max_length = 50)