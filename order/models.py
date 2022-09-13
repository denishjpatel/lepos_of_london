from django.db import models
from user.models import *
from product.models import *

# Create your models here.

class Order(models.Model):
    status_list = [
        ('Pending For Payment','Pending For Payment'),
        ("Confirmed","Confirmed")
    ]
    user = models.ForeignKey(Account, on_delete=models.SET_NULL, null=True)
    payment_method = models.CharField(max_length=200, null=True, blank=True)
    order_id = models.CharField(max_length=20, unique=True, editable=False)
    
    shipping_price = models.DecimalField(
        max_digits=8, decimal_places=2, null=True, blank=True)
    total_price = models.DecimalField(
        max_digits=8, decimal_places=2, null=True, blank=True)
    status = models.CharField(choices=status_list,max_length=100)
    
    is_delivered = models.BooleanField(default=False)
    delivered_at = models.DateTimeField(
        auto_now_add=False, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    # address_id = models.IntegerField(default=0,null=True,blank=True)

    def __str__(self):
        return "{} has placed order with {} and price {} with id {} ".format(self.user,self.payment_method,self.total_price,self.pk)

    def get_order_items(self):
        items = OrderItem.objects.filter(order=self)
        print(items)
        return items
    def get_order_item_count(self):
        count = OrderItem.objects.filter(order=self).count()
        return count


class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, null=True,related_name='orderitem')
    # name = models.CharField(max_length=200, null=True, blank=True)
    qty = models.IntegerField(null=True, blank=True, default=0)
    unit_price = models.DecimalField(
        max_digits=20, decimal_places=2, null=True, blank=True)
    sub_total = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True)
    # id = models.AutoField(primary_key=True, editable=False)

    def __str__(self):
        return str(self.product.name)

class OrderAddress(models.Model):
    order = models.OneToOneField(Order,on_delete=models.CASCADE,related_name='orderaddress')
    address = models.CharField(max_length=200, null=True, blank=True)
    pincode = models.CharField(max_length=200, null=True, blank=True)
    city = models.CharField(max_length=200, null=True, blank=True)
    state = models.CharField(max_length=200, null=True, blank=True)
    country = models.CharField(max_length=200, null=True, blank=True)
    shippingPrice = models.DecimalField(
        max_digits=7, decimal_places=2, null=True, blank=True)
    # id = models.AutoField(primary_key=True, editable=False)

    def __str__(self):
        return str(self.address)
    
class guest_user(models.Model):
    first_name = models.CharField(max_length=200, null=True, blank=True)
    last_name = models.CharField(max_length=200, null=True, blank=True)
    contact_number = models.CharField(max_length=200, null=True, blank=True)
    email = models.CharField(max_length=200, null=True, blank=True)
    order = models.OneToOneField(Order,on_delete=models.CASCADE, null=True, blank=True)
    address = models.CharField(max_length=200, null=True, blank=True)
    pincode = models.CharField(max_length=200, null=True, blank=True)
    city = models.CharField(max_length=200, null=True, blank=True)
    state = models.CharField(max_length=200, null=True, blank=True)
    country = models.CharField(max_length=200, null=True, blank=True)
    shippingPrice = models.DecimalField(
        max_digits=7, decimal_places=2, null=True, blank=True)