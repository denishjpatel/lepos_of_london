from django.contrib import admin
from .models import *
# Register your models here.

class AddressAdmin(admin.ModelAdmin):
    list_display = ('user','city')
    list_display_links = ('user','city')

admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(CartAddress,AddressAdmin)