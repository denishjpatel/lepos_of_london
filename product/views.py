from django.http import JsonResponse
from django.http.response import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from .models import *
from user.models import *
from django.core.paginator import PageNotAnInteger,Paginator,EmptyPage
from django.db.models import Q

# Create your views here.

def index(request):
    products = Product.objects.all()
    last_products = Product.objects.all().order_by('-created_at')[:3]
    first_products = Product.objects.all()[0:3]
    
    website_users = WebsiteUser.objects.first()
    index_images = Index_image.objects.first()
    qoute_data = Quote.objects.first()
    future_section = FutureSection.objects.first()
    bespoke_jewellery = BespokeJewellery.objects.first()
    sustainable_essentials = SustainableEssentials.objects.first()
    contact_data = Contact.objects.first()
    
    return render(request,"edge_index.html",{"products":products,"last_products":last_products,"first_products":first_products, "website_users":website_users, "index_images":index_images, "qoute_data":qoute_data, "future_section":future_section, "bespoke_jewellery":bespoke_jewellery, "sustainable_essentials":sustainable_essentials, "contact_data":contact_data})

def products(request):
    products = Product.objects.all()
    
    if 'category' in request.GET:
        category = request.GET['category']
        products = Product.objects.filter(category__title = category)
        category = Category.objects.get(title=category)
        return render(request,"edge_shop.html",{"products":products, "category":category})
    
    if 'search' in request.GET:
        searchvalue = request.GET['search']
        products = Product.objects.filter(Q(name__icontains=searchvalue) | Q(sub_title__icontains=searchvalue))
    
    # paginator = Paginator(products, 6)
    # page = request.GET.get('page')
    # products = paginator.get_page(page)
    return render(request,"edge_shop.html",{"products":products})

def product_details(request,id):
    
        
    bespoke_jewellery = BespokeJewellery.objects.first()

    product = Product.objects.get(id=int(id))
    contact_data = Contact.objects.first()


    if request.method=="POST":
        name = request.POST.get("name")
        title = request.POST.get("title")
        product_review = request.POST.get("product_review")
        ratings = request.POST["ratings"]
        Review.objects.create(product=product, title=title, product_review=product_review, ratings=ratings)
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    similar_prods = Product.objects.filter(category=product.category)[:6]
    reviews = Review.objects.filter(product=product)
    return render(request,"edge_product.html",{"product":product, "similar_prods":similar_prods, "reviews":reviews, "bespoke_jewellery":bespoke_jewellery, "contact_data":contact_data})

def about(request):
    return render(request,"edge_about.html")

def show_wishlist(request):
    if request.user.is_authenticated:
        wishlist_obj = wishlist.objects.filter(user=request.user)
        return render(request,"edge_wishlist.html", {"wishlist_data" : wishlist_obj})
    else:
        return redirect("loginview")    

def add_wishlist(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            id = request.POST['id']
            prod_obj = Product.objects.get(id=id)
            try:
                wishlist.objects.get(user=request.user, product=prod_obj)
                return JsonResponse({"error":"Product already exists in wishlist!"})
            except:
                wishlist.objects.create(user=request.user, product=prod_obj)
                return JsonResponse({"success":"Product added to wishlist"})
    else:
        return redirect("loginview")
    # return render(request,"wishlist.html")