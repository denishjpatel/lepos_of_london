from django.contrib import admin
from . models import *

# Register your models here.
class ImageInliner(admin.TabularInline):
    model = ProductImages
    extra = 1
    
class ImageInliner1(admin.TabularInline):
    model = SliderImages
    extra = 1
    
class ProductAdmin(admin.ModelAdmin):
    inlines = (ImageInliner,)
    
class IndexImageAdmin(admin.ModelAdmin):
    inlines = (ImageInliner1,)
    
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('pk','title')
    list_display_links = ('pk','title')
    
class GoldFilterAdmin(admin.ModelAdmin):
    list_display = ('product', 'colour', 'purity')
    list_display_links = ('product',)
    
admin.site.register(Category)
admin.site.register(wishlist)
admin.site.register(Product, ProductAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(GoldFilter, GoldFilterAdmin)
admin.site.register(Index_image, IndexImageAdmin)
admin.site.register(LeposLondonUser)