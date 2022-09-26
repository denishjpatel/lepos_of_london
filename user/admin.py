from django.contrib import admin
from .models import *

# Register your models here.
class AddressAdmin(admin.ModelAdmin):
    list_display = ('city', 'user')
    list_display_links = ('city', 'user')

admin.site.register(Account)
admin.site.register(Contact)
admin.site.register(Address, AddressAdmin)