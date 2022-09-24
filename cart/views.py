from django.shortcuts import render, redirect, get_object_or_404, reverse
from .models import *
from user.models import *
from product.models import *
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
from django.http.response import JsonResponse
from django.contrib.auth import get_user_model
# Create your views here.
User = get_user_model()

def _cart_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart

def cart(request, total=0, quantity=0, cart_items=None):
    try:
        tax = 0
        grand_total = 0
        if request.user.is_authenticated:
            cart_items = CartItem.objects.filter(user=request.user, is_active=True)
        else:
            cart = Cart.objects.get(cart_id=_cart_id(request))
            cart_items = CartItem.objects.filter(cart=cart, is_active=True)
            
        for cart_item in cart_items:
            total += (cart_item.unit_price * cart_item.quantity)
            quantity += cart_item.quantity
        tax = 0
        grand_total = total + tax
    except ObjectDoesNotExist:
        pass #just ignore

    context = {
        'total': total,
        'quantity': quantity,
        'cart_items': cart_items,
        'tax'       : tax,
        'grand_total': grand_total,
    }
    return render(request, 'cart.html', context)

def add_cart(request,product_id):
    if request.method == "POST":
        product_price = request.POST["hidden_price"]
        metal_val = request.POST["hidden_metal"]
        quantity = request.POST["quantity"]
        
        if request.user.is_authenticated:
            product = Product.objects.get(id=product_id)
            try:
                cart_item = CartItem.objects.get(product=product,user = request.user)
                cart_item.quantity += 1
                cart_item.save()
            except:
                cart_item = CartItem.objects.create(
                    product = product,
                    user = request.user,
                    unit_price=product_price,
                    quantity=quantity,
                    metal=metal_val
                )
                cart_item.save()
            
            return redirect('cart')


        else:
            product = Product.objects.get(id=product_id)
            try:
                cart = Cart.objects.get(cart_id=_cart_id(request))
            except Cart.DoesNotExist:
                cart = Cart.objects.create(
                    cart_id = _cart_id(request)
                )
            cart.save()
            
            try:
                cart_item = CartItem.objects.get(product=product,cart=cart, unit_price=product.metal_14_price)
                cart_item.quantity += 1
                cart_item.save()
            except:
                cart_item = CartItem.objects.create(
                    product = product,
                    quantity = 1,
                    cart = cart,
                    unit_price=product.metal_14_price,
                )
                cart_item.save()
            
            return redirect('cart')
    
    else:
        messages.error(request,"Not Valid Method")
        return redirect('buyProduct')

def IncQuntity(request,val,id):
    try:       
        cart_item = CartItem.objects.get(pk=id)
        cart_item.quantity = int(val)
        cart_item.save()
        if request.user.is_authenticated:
            cart_items = CartItem.objects.filter(user=request.user, is_active=True)
        else:
            cart = Cart.objects.get(cart_id=_cart_id(request))
            cart_items = CartItem.objects.filter(cart=cart, is_active=True)
        total =0 
        quantity =0 
        for cart_item1 in cart_items:
            total += (cart_item1.unit_price * cart_item1.quantity)
            quantity += cart_item1.quantity
        tax = 0
        grand_total = total + tax
        sub_total = cart_item.quantity * cart_item.unit_price
        return JsonResponse({'msg':'success','sub_total':sub_total,'total':total,'grand_total':grand_total})

    except CartItem.DoesNotExist:
        return JsonResponse({'msg':'error'})
    
def remove_cart_item(request, product_id, cart_item_id):
    product = get_object_or_404(Product, id=product_id)
    if request.user.is_authenticated:
        cart_item = CartItem.objects.get(product=product, user=request.user, id=cart_item_id)
    else:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_item = CartItem.objects.get(product=product, cart=cart, id=cart_item_id)
    cart_item.delete()
    return redirect('cart')

# def proceed_to_order(request):
#     if request.user.is_authenticated:
#         # address = CartAddress.objects.filter(user=request.user).last()
#         total = 0
#         quantity = 0
#         try:
#             tax = 0
#             grand_total = 0
#             if request.user.is_authenticated:
#                 cart_items = CartItem.objects.filter(user=request.user, is_active=True)
#             else:
#                 cart = Cart.objects.get(cart_id=_cart_id(request))
#                 cart_items = CartItem.objects.filter(cart=cart, is_active=True)
#             for cart_item in cart_items:
#                 total += (cart_item.unit_price * cart_item.quantity)
#                 quantity += cart_item.quantity
#             tax = 0
#             grand_total = total + tax
#         except ObjectDoesNotExist:
#             pass #just ignore

#         context = {
#             'total': total,
#             'quantity': quantity,
#             'cart_items': cart_items,
#             'tax'       : tax,
#             'grand_total': grand_total
#         }
#         return render(request,"order.html",context)
#     else:
#         pass