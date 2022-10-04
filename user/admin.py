from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *

# Register your models here.
class AddressAdmin(admin.ModelAdmin):
    list_display = ('city', 'user')
    list_display_links = ('city', 'user')


class CustomUserAdmin(UserAdmin):
    fieldsets = (
        *UserAdmin.fieldsets,  # original form fieldsets, expanded
        (                      # new fieldset added on to the bottom
            'Admin User Actions',  # group heading of your choice; set to None for a blank space instead of a header
            {
                'fields': (
                    'contact_number',
                    'dob',
                    'gender',
                ),
            },
        ),
    )


admin.site.register(Account,CustomUserAdmin)
admin.site.register(Contact)
admin.site.register(terms_conditions)
admin.site.register(Address, AddressAdmin)