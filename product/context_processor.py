from django.http import HttpResponse
from .models import *

def all_categories(request):
    categories = Category.objects.all()
    return {'categories':categories}

def wishlist_count(request):
    wishlist_obj = None
    if request.user.is_authenticated:
        wishlist_obj = wishlist.objects.filter(user=request.user)
    return {'wishlist_count':wishlist_obj}