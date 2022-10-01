from django.db import models
from user.models import *
from product.models import *

# Create your models here.

class Cart(models.Model):
    cart_id = models.CharField(max_length=250, blank=True)
    date_added = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.cart_id


class CartItem(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, null=True)
    quantity = models.IntegerField()
    material = models.IntegerField(null=True, blank=True)
    size = models.IntegerField(null=True, blank=True)
    unit_price = models.DecimalField(max_digits=20,decimal_places=2)
    is_active = models.BooleanField(default=True)

    def sub_total(self):
        return self.unit_price * self.quantity

    def __unicode__(self):
        return self.product

class CartAddress(models.Model):
    user = models.ForeignKey(Account,on_delete=models.CASCADE)
    address = models.CharField(max_length=200, null=True, blank=True)
    pincode = models.CharField(max_length=200, null=True, blank=True)
    city = models.CharField(max_length=200, null=True, blank=True)
    state = models.CharField(max_length=200, null=True, blank=True)
    country = models.CharField(max_length=200, null=True, blank=True)

    shippingPrice = models.DecimalField(
        max_digits=7, decimal_places=2, null=True, blank=True)
    id = models.AutoField(primary_key=True, editable=False)

    def __str__(self):
        return str(self.address)
