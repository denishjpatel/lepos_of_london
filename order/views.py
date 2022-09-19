from multiprocessing import context
from django.shortcuts import render
from user.models import *
from product.models import *
from cart.models import *
from .models import *
from django.contrib.auth import get_user_model
from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.contrib import messages
from django.http import HttpResponse
from cart.views import _cart_id
from datetime import datetime, timedelta, date
import razorpay
from django.core.exceptions import ObjectDoesNotExist

# Create your views here.
User = get_user_model()

from random import randint

def random_with_N_digits(n):
    range_start = 10**(n-1)
    range_end = (10**n)-1
    return randint(range_start, range_end)

def order(request):
    # try:
    #     cart = Cart.objects.get(cart_id=_cart_id(request))
    # except:
    #     cart = None
    if request.user.is_authenticated:
        total = 0
        tax = 0
        grand_total = 0
        
        if request.method=="POST":
            print("inside payment")
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            email = request.POST.get('email')
            contact_number = request.POST.get('contact_number')
            address = request.POST.get('address')
            city = request.POST.get('city')
            pincode = request.POST.get('pincode')
            state = request.POST.get('state')
            country = request.POST.get('country')
                        
            user_obj = User.objects.get(username=request.user)
            user_obj.first_name = first_name
            user_obj.last_name = last_name
            user_obj.email = email
            user_obj.contact_number = contact_number
            user_obj.save()
            
            add_obj = Address.objects.create(user=user_obj)
            add_obj.address = address
            add_obj.city = city
            add_obj.pincode = pincode
            add_obj.state = state
            add_obj.country = country
            add_obj.save()
            
            payment_method="COD"
            order_id=f'order_cod_{random_with_N_digits(6)}'
            total_price=request.POST.get('total_price')
            
            order_obj = Order.objects.create(
                user = request.user,
                payment_method = payment_method,
                order_id = order_id,
                shipping_price = 0,
                total_price = total_price,
                status = "Pending For Payment",
                delivered_at = date.today() + timedelta(days=10)
            )
            
            sub_total = request.POST.get('sub_total')
            prods = request.POST.getlist('ids[]')
            qtys = request.POST.getlist('qty[]')
            unit_prices = request.POST.getlist('unit_price[]')
            
            for i in range(len(prods)):
                prod_obj = Product.objects.get(id=prods[i])
                order_item_obj = OrderItem.objects.create(
                    product = prod_obj,
                    order = order_obj,
                    qty = qtys[i],
                    unit_price = unit_prices[i],
                    sub_total = sub_total,
                )
            
            cart_add = OrderAddress.objects.create(
                order=order_obj,
                address = address,
                city = city,
                pincode = pincode,
                state = state,
                country = country
            )
            
            cartitem_obj = CartItem.objects.filter(user=request.user)
            cartitem_obj.delete()
            return redirect('my_orders')
        
        elif request.method == "GET":
            user_obj = User.objects.get(username=request.user)
            try:
                add_obj = Address.objects.get(user=user_obj)
            except:
                add_obj = None
                
            try:
                cartitem_obj = CartItem.objects.filter(user=user_obj)
                for i in cartitem_obj:
                    total += (i.unit_price * i.quantity)
                grand_total = total + tax
            except Exception as e:
                cartitem_obj = None
            
            client = razorpay.Client(auth=("rzp_test_nGsms8YvPMJW4g", "DJqTA9Sr17mpAMg8ZiO28i8l"))
            para = {
                "amount": int(grand_total),
                "currency": "INR"
            }
            order_id = client.order.create(data=para)
            context = {
                "order_id" : order_id,
                "user_data": user_obj,
                "add_data": add_obj,
                "cartitem_data":cartitem_obj,
                "total":total,
                'grand_total':grand_total
            }
                
            return render(request, "edge_order.html", context)
        
        else:
            return HttpResponse("Method Not Allowed!!!")
    else:
        total = 0
        tax = 0
        grand_total = 0
        
        if request.method=="POST":
            print("got it")
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            email = request.POST.get('email')
            contact_number = request.POST.get('contact_number')
            address = request.POST.get('address')
            city = request.POST.get('city')
            pincode = request.POST.get('pincode')
            state = request.POST.get('state')
            country = request.POST.get('country')
            
            payment_method="COD"
            order_id=f'order_cod_{random_with_N_digits(6)}'
            total_price=request.POST.get('total_price')
            
            order_obj = Order.objects.create(
                # user = request.user,
                payment_method = payment_method,
                order_id = order_id,
                shipping_price = 0,
                total_price = total_price,
                status = "Pending For Payment",
                delivered_at = date.today() + timedelta(days=10)
            )
            print("order object==>", order_obj)
            
            guest_user_obj = guest_user.objects.create(
                first_name = first_name,
                last_name = last_name,
                email = email,
                contact_number = contact_number,
                address = address,
                city = city,
                pincode = pincode,
                state = state,
                country = country,
                order = order_obj
            )
            
            sub_total = request.POST.get('sub_total')
            prods = request.POST.getlist('ids[]')
            qtys = request.POST.getlist('qty[]')
            unit_prices = request.POST.getlist('unit_price[]')
            
            for i in range(len(prods)):
                prod_obj = Product.objects.get(id=prods[i])
                order_item_obj = OrderItem.objects.create(
                    product = prod_obj,
                    order = order_obj,
                    qty = qtys[i],
                    unit_price = unit_prices[i],
                    sub_total = sub_total,
                )
            
            
            cart = Cart.objects.get(cart_id=_cart_id(request))
            cartitem_obj = CartItem.objects.filter(cart=cart, is_active=True)
            cartitem_obj.delete()
            messages.info(request,"Your order is placed.")
            return redirect('index')
        
        if request.method == "GET":
            print("inside get")
            total = 0
            quantity = 0
            try:
                tax = 0
                grand_total = 0
                if request.user.is_authenticated:
                    cartitem_obj = CartItem.objects.filter(user=request.user, is_active=True)
                else:
                    cart = Cart.objects.get(cart_id=_cart_id(request))
                    cartitem_obj = CartItem.objects.filter(cart=cart, is_active=True)
                for cart_item in cartitem_obj:
                    total += (cart_item.unit_price * cart_item.quantity)
                    quantity += cart_item.quantity
                tax = 0
                grand_total = total + tax
            except ObjectDoesNotExist:
                pass #just ignore
            
            client = razorpay.Client(auth=("rzp_test_T15HUukxUCbpYR", "trw9b5ZJ8zXZIdpQgrBB42cE"))
            para = {
                "amount": int(grand_total),
                "currency": "INR"
            }
            order_id = client.order.create(data=para)

            # context = {
            #     'total': total,
            #     'quantity': quantity,
            #     'tax'       : tax,
            #     "cartitem_data":cartitem_obj,
            #     'grand_total': grand_total
            # }
            
            context = {
                "order_id" : order_id,
                "cartitem_data":cartitem_obj,
                "total":total,
                'grand_total':grand_total
            }
            return render(request,"edge_order.html",context)
            
            
    # else:
    #     messages.info(request,"Please Make Login First to Procced Order!")
    #     return redirect(reverse("loginview") + "?url=order" + f"?request_data={cart}")
    
def pay_razorpay(request):
    print("inside razorpay")
    # try:
    #     cart = Cart.objects.get(cart_id=_cart_id(request))
    # except:
    #     cart = None
    if request.user.is_authenticated:
        if request.method == "POST":
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            email = request.POST.get('email')
            contact_number = request.POST.get('contact_number')
            address = request.POST.get('address')
            city = request.POST.get('city')
            pincode = request.POST.get('pincode')
            state = request.POST.get('state')
            country = request.POST.get('country')
                        
            user_obj = User.objects.get(username=request.user)
            user_obj.first_name = first_name
            user_obj.last_name = last_name
            user_obj.email = email
            user_obj.contact_number = contact_number
            user_obj.save()
            
            add_obj = Address.objects.get(user=user_obj)
            add_obj.address = address
            add_obj.city = city
            add_obj.pincode = pincode
            add_obj.state = state
            add_obj.country = country
            add_obj.save()
            
            payment_method=request.POST.get('payment_mode')
            order_id=request.POST.get('order_id')
            total_price=request.POST.get('total_price')
            
            order_obj = Order.objects.create(
                user = request.user,
                payment_method = payment_method,
                order_id = order_id,
                shipping_price = 0,
                total_price = total_price,
                status = "Confirmed",
                delivered_at = date.today() + timedelta(days=10)
            )
            
            sub_total = request.POST.get('sub_total')
            prods = request.POST.getlist('ids[]')
            qtys = request.POST.getlist('qtys[]')
            unit_prices = request.POST.getlist('unit_prices[]')
            
            for i in range(len(prods)):
                prod_obj = Product.objects.get(id=prods[int(i)])
                order_item_obj = OrderItem.objects.create(
                    product = prod_obj,
                    order = order_obj,
                    qty = qtys[int(i)],
                    unit_price = unit_prices[int(i)],
                    sub_total = sub_total,
                )
            
            cart_add = OrderAddress.objects.create(
                order=order_obj,
                address = address,
                city = city,
                pincode = pincode,
                state = state,
                country = country
            )
            
            cartitem_obj = CartItem.objects.filter(user=request.user)
            cartitem_obj.delete()
            return redirect('index')
        else:
            return HttpResponse("Method Not Allowed!!!")
        
    else:
        if request.method == "POST":
            print("yes")
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            email = request.POST.get('email')
            contact_number = request.POST.get('contact_number')
            address = request.POST.get('address')
            city = request.POST.get('city')
            pincode = request.POST.get('pincode')
            state = request.POST.get('state')
            country = request.POST.get('country')
            
            payment_method=request.POST.get('payment_mode')
            order_id=request.POST.get('order_id')
            total_price=request.POST.get('total_price')
            
            order_obj = Order.objects.create(
                payment_method = payment_method,
                order_id = order_id,
                shipping_price = 0,
                total_price = total_price,
                status = "Confirmed",
                delivered_at = date.today() + timedelta(days=10)
            )
                        
            user_obj = guest_user.objects.create(
                first_name = first_name,
                last_name = last_name,
                email = email,
                contact_number = contact_number,
                address = address,
                city = city,
                pincode = pincode,
                state = state,
                country = country,
                order=order_obj
            )
            
            sub_total = request.POST.get('sub_total')
            prods = request.POST.getlist('ids[]')
            qtys = request.POST.getlist('qtys[]')
            unit_prices = request.POST.getlist('unit_prices[]')
            
            for i in range(len(prods)):
                prod_obj = Product.objects.get(id=prods[int(i)])
                order_item_obj = OrderItem.objects.create(
                    product = prod_obj,
                    order = order_obj,
                    qty = qtys[int(i)],
                    unit_price = unit_prices[int(i)],
                    sub_total = sub_total,
                )
            
            cart = Cart.objects.get(cart_id=_cart_id(request))
            cartitem_obj = CartItem.objects.filter(cart=cart, is_active=True)
            cartitem_obj.delete()
            return redirect('index')
        else:
            return HttpResponse("Method Not Allowed!!!")
        
    # else:
    #     messages.info(request,"Please Make Login First to Procced Order!")
    #     return redirect(reverse("loginview") + "?url=order" + f"?request_data={cart}")
    
def my_orders(request):
    if request.user.is_authenticated:
        order_obj = Order.objects.filter(user=request.user)
        orderitems = []
        for i in order_obj:
            orderitem_obj = OrderItem.objects.filter(order = i)
            for j in orderitem_obj:
                orderitems.append(j)

        context = {
            "order_data":order_obj,
            "orderitem_data":reversed(orderitems),
        }
        return render(request, "edge_my_orders.html", context)
    
    else:
        messages.info(request,"Please Make Login First to See Your Orders!")
        return redirect(reverse("loginview") + "?url=my_orders")