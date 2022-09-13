from django.db import models
from user.models import Account, models
from django.core.validators import MinValueValidator, MaxValueValidator
# Create your models here.

class Category(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
    
class Product(models.Model):
    type_choice = [
        ('Gold','Gold'),
        ('Silver','Silver'),
        ('Platinum','Platinum'),
    ]
    
    name = models.CharField(max_length=200,unique=True)
    price = models.IntegerField(null=True, blank=True)
    category = models.ForeignKey(Category,on_delete=models.CASCADE)
    image = models.ImageField(upload_to="product")
    video = models.FileField(upload_to="product", null=True, blank=True)
    metal = models.CharField(choices=type_choice,max_length=9,null=True,blank=True, default=type_choice[1][1])
    size = models.IntegerField(default=1, validators=[MinValueValidator(1), MaxValueValidator(4)],null=True,blank=True)
    in_stock = models.BooleanField(default=True)
    product_description = models.TextField(null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name
    
    def get_images(self):
        return ProductImages.objects.filter(product=self)
    
    def get_goldfilter(self):
        return GoldFilter.objects.get(product=self)
        
class ProductImages(models.Model):
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    image = models.ImageField(upload_to = 'product')

class Review(models.Model):
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    user = models.ForeignKey(Account,on_delete=models.CASCADE)
    ratings = models.IntegerField()
    title = models.CharField(max_length=200,null=True,blank=True)
    product_review = models.TextField(null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.pk
    
class wishlist(models.Model):
    user = models.ForeignKey(Account,on_delete=models.CASCADE, null=True,blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True,blank=True)
    create_at = models.DateTimeField(auto_now_add=True, null=True,blank=True)
    
class GoldFilter(models.Model):
    colour_choice = [
        ('rose','rose'),
        ('yellow','yellow'),
        ('white','white'),
    ]
    
    purity_choice = [
        ('14','14'),
        ('16','16'),
        ('18','18'),
        ('20','20'),
    ]

    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True,blank=True)
    colour = models.CharField(choices=colour_choice,max_length=7,null=True,blank=True)
    purity = models.CharField(choices=purity_choice,max_length=3,null=True,blank=True)