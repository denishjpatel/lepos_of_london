from django.http import JsonResponse
from django.http.response import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from .models import *
from django.core.paginator import PageNotAnInteger,Paginator,EmptyPage

# Create your views here.

def index(request):
    products = Product.objects.all()
    last_products = Product.objects.all().order_by('-created_at')[:3]
    first_products = Product.objects.all()[0:3]
    print(last_products)
    print(first_products)
    
    return render(request,"edge_index.html",{"products":products,"last_products":last_products,"first_products":first_products})

def products(request):
    if 'category' in request.GET:
        category = request.GET['category']
        products = Product.objects.filter(category__title = category)
        category = Category.objects.get(title=category)
        return render(request,"products.html",{"products":products, "category":category})
    
    products = Product.objects.all()
    # paginator = Paginator(products, 6)
    # page = request.GET.get('page')
    # products = paginator.get_page(page)
    return render(request,"edge_shop.html",{"products":products})

def product_details(request,id):
    product = Product.objects.get(id=id)
    if request.method=="POST":
        name = request.POST.get("name")
        title = request.POST.get("title")
        product_review = request.POST.get("product_review")
        ratings = request.POST["ratings"]
        Review.objects.create(product=product, title=title, product_review=product_review, ratings=ratings)
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    
    similar_prods = Product.objects.filter(category=product.category)[:6]
    reviews = Review.objects.filter(product=product)
    return render(request,"edge_product.html",{"product":product, "similar_prods":similar_prods, "reviews":reviews})

def about(request):
    return render(request,"edge_about.html")

def show_wishlist(request):
    if request.user.is_authenticated:
        wishlist_obj = wishlist.objects.filter(user=request.user)
        return render(request,"wishlist.html", {"wishlist_data" : wishlist_obj})
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