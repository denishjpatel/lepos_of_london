from django.contrib import admin
from . models import *

# Register your models here.
class ImageInliner(admin.TabularInline):
    model = ProductImages
    extra = 1

class SizeInliner(admin.TabularInline):
    model = ProductSize
    extra = 1
    
class ImageInliner1(admin.TabularInline):
    model = SliderImages
    extra = 1
    
class TextInliner(admin.TabularInline):
    model = BespokeText
    extra = 1
    
class FreeShippingTextInliner(admin.TabularInline):
    model = FreeShippingText
    extra = 1
    
class ProductAdmin(admin.ModelAdmin):
    inlines = (ImageInliner,SizeInliner)
    
class IndexImageAdmin(admin.ModelAdmin):
    inlines = (ImageInliner1,)
    
class TextInlinerAdmin(admin.ModelAdmin):
    inlines = (TextInliner,)
    
class FreeShippingTextInlinerAdmin(admin.ModelAdmin):
    inlines = (FreeShippingTextInliner,)
    
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('pk','title')
    list_display_links = ('pk','title')
    
# class GoldFilterAdmin(admin.ModelAdmin):
#     list_display = ('product', 'colour', 'purity')
#     list_display_links = ('product',)
    
admin.site.register(Category)
admin.site.register(wishlist)
admin.site.register(Product, ProductAdmin)
admin.site.register(Review, ReviewAdmin)
# admin.site.register(GoldFilter, GoldFilterAdmin)
admin.site.register(Index_image, IndexImageAdmin)
admin.site.register(Quote)
admin.site.register(BespokeJewellery, TextInlinerAdmin)
admin.site.register(FutureSection)
admin.site.register(WebsiteUser)
admin.site.register(SustainableEssentials)
admin.site.register(ProductSustainableEssentials)
admin.site.register(HeaderSliderText)
admin.site.register(FreeShipping, FreeShippingTextInlinerAdmin)