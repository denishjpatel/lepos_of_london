from django.http import HttpResponse
from .models import *
from user.models import *

def all_categories(request):
    categories = Category.objects.all()
    contact_data = Contact.objects.first()

    return {'categories':categories, "contact_data":contact_data}

def wishlist_count(request):
    print("got it")
    wishlist_obj = None
    if request.user.is_authenticated:
        print("inside it")
        wishlist_obj = wishlist.objects.filter(user=request.user)
    return {'wishlist_count':wishlist_obj}