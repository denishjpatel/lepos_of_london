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
    # type_choice = [
    #     ('Gold','Gold'),
    #     ('Silver','Silver'),
    #     ('Platinum','Platinum'),
    # ]
    
    material_choice = [
        ('10','10'),
        ('14','14'),
        ('18','18')
    ]
    
    name = models.CharField(max_length=200,unique=True)
    sub_title = models.CharField(max_length=100, blank=True, null=True)
    material_10_price = models.IntegerField(null=True, blank=True)
    material_14_price = models.IntegerField(null=True, blank=True)
    material_18_price = models.IntegerField(null=True, blank=True)
    category = models.ForeignKey(Category,on_delete=models.CASCADE)
    image = models.ImageField(upload_to="product")
    # video = models.FileField(upload_to="product", null=True, blank=True)
    material = models.CharField(choices=material_choice,max_length=9,null=True,blank=True, default=material_choice[1][1])
    # size = models.IntegerField(default=1, validators=[MinValueValidator(1), MaxValueValidator(4)],null=True,blank=True)
    quantity = models.IntegerField(default=1, validators=[MinValueValidator(1), MaxValueValidator(4)],null=True,blank=True)
    in_stock = models.BooleanField(default=True)
    is_size = models.BooleanField(default=False)
    product_description = models.TextField(null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name
    
    def get_images(self):
        return ProductImages.objects.filter(product=self)
    
    def get_sizes(self):
        return ProductSize.objects.filter(p_size=self)
    
    # def get_goldfilter(self):
    #     return GoldFilter.objects.get(product=self)
        
class ProductImages(models.Model):
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    image = models.ImageField(upload_to = 'product')
    
class ProductSize(models.Model):
    p_size = models.ForeignKey(Product,on_delete=models.CASCADE)
    size = models.IntegerField(default=1)

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
    
# class GoldFilter(models.Model):
    # colour_choice = [
    #     ('rose','rose'),
    #     ('yellow','yellow'),
    #     ('white','white'),
    # ]
    
    # purity_choice = [
    #     ('14','14'),
    #     ('16','16'),
    #     ('18','18'),
    #     ('20','20'),
    # ]

    # product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True,blank=True)
    # colour = models.CharField(choices=colour_choice,max_length=7,null=True,blank=True)
    # purity = models.CharField(choices=purity_choice,max_length=3,null=True,blank=True)
    
class Index_image(models.Model):
    necklace_image = models.ImageField(upload_to = 'product')
    earring_image = models.ImageField(upload_to = 'product')
    ring_image = models.ImageField(upload_to = 'product')
    bracelet_image = models.ImageField(upload_to = 'product')

    def save(self, *args, **kwargs):
        if self.__class__.objects.count():
            self.pk = self.__class__.objects.first().pk
        super().save(*args, **kwargs)
        
    def get_slider_images(self):
        return SliderImages.objects.filter(index_img=self)
        
class SliderImages(models.Model):
    index_img = models.ForeignKey(Index_image,on_delete=models.CASCADE)
    slider_image = models.ImageField(upload_to = 'product')
    
    
class Quote(models.Model):
    title1 = models.CharField(max_length=255)
    title2 = models.CharField(max_length=255)
    title3 = models.CharField(max_length=255)
    text1 = models.CharField(max_length=255)
    text2 = models.CharField(max_length=255, null=True, blank=True)
    text3 = models.CharField(max_length=255, null=True, blank=True)
    

class BespokeJewellery(models.Model):
    title = models.CharField(max_length=255)
    sub_title = models.CharField(max_length=255)
    text1 = models.CharField(max_length=255, null=True, blank=True)
    text2 = models.CharField(max_length=255, null=True, blank=True)
    text3 = models.CharField(max_length=255, null=True, blank=True)
    bespoke_video = models.FileField(upload_to = 'product')
    
    
class FutureSection(models.Model):
    title = models.CharField(max_length=255)
    sub_title = models.CharField(max_length=255)
    text1 = models.CharField(max_length=255)
    text2 = models.CharField(max_length=255)
    text3 = models.CharField(max_length=255)
    image = models.ImageField(max_length=255)
    

class WebsiteUser(models.Model):
    title = models.CharField(max_length=255)
    image1 = models.ImageField(upload_to = 'product')
    name1 = models.CharField(max_length=255)
    image2 = models.ImageField(upload_to = 'product')
    name2 = models.CharField(max_length=255)
    image3 = models.ImageField(upload_to = 'product')
    name3 = models.CharField(max_length=255)
    image4 = models.ImageField(upload_to = 'product')
    name4 = models.CharField(max_length=255)
    
    
class SustainableEssentials(models.Model):
    title = models.CharField(max_length=255)
    image = models.ImageField(max_length=255)
    

class ProductSustainableEssentials(models.Model):
    title = models.CharField(max_length=255)
    image = models.ImageField(max_length=255)
    
        
class HeaderSliderText(models.Model):
    text1 = models.CharField(max_length = 50)
    text2 = models.CharField(max_length = 50)