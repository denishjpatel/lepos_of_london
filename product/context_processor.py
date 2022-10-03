from django.http import HttpResponse
from .models import *
from user.models import *

def all_categories(request):
    categories = Category.objects.all()
    contact_data = Contact.objects.first()
    header_slider_text_data = HeaderSliderText.objects.first()

    return {'categories':categories, "contact_data":contact_data, "header_slider_text_data":header_slider_text_data}

def wishlist_count(request):
    wishlist_obj = None
    if request.user.is_authenticated:
        wishlist_obj = wishlist.objects.filter(user=request.user)
    return {'wishlist_count':wishlist_obj}