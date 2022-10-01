from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, reverse
from django.contrib.auth import login, authenticate, get_user_model, logout, update_session_auth_hash
from django.contrib import messages
from django.contrib.auth.hashers import check_password, make_password
from user.models import *
from cart.models import *
from cart.views import _cart_id
# Create your views here.
User = get_user_model()


def loginview(request):
    if not request.user.is_authenticated:
        if request.method == "POST":
            username = request.POST['username']
            password = request.POST['password']

            if User.objects.filter(username=username).exists():
                if authenticate(username=username, password=password):
                    user = authenticate(username=username, password=password)
                    login(request, user)
                    
                    if 'url' in request.GET:
                        url_data = request.GET['url']
                        str1 = url_data.replace("=","?")
                        res = str1.split("?")
                        try:
                            cart = Cart.objects.get(cart_id=res[2])
                            cart_items = CartItem.objects.filter(cart=cart, is_active=True)
                            for i in cart_items:
                                i.user=request.user
                                i.save()
                        except Exception as e:
                            print(e)
                        messages.success(request, 'Successfully Login')
                        return redirect(res[0])
                    messages.success(request, 'Successfully Login')
                    return redirect('index')         
                else:
                    messages.error(
                        request, "You have entered wrong password!!!")
                    return redirect('loginview')
            else:
                messages.error(request, "Username not found!!!")
                return redirect('loginview')
        return render(request, "edge_login.html")
    else:
        return redirect("index")


def register(request):
    if not request.user.is_authenticated:
        if request.method == "POST":
            username = request.POST['username']
            last_name = request.POST('last_name')
            first_name = request.POST('first_name')
            email = request.POST['email']
            contact = request.POST['contact']
            password = request.POST['password']
            confirm_password = request.POST['confirm_password']

            if password == confirm_password:
                if User.objects.filter(username=username).exists():
                    messages.error(request, 'Username already exists!!!')
                    return redirect('register')
                if User.objects.filter(email=email).exists():
                    messages.error(request, 'Email already exists!!!')
                    return redirect('register')
                user = User.objects.create_user(
                    username=username, last_name=last_name, first_name=first_name, email=email, contact_number=contact, password=password)
                user.save()
                login(request, user)
                messages.success(request, 'Successfully Registered')
                return redirect('index')
            else:
                messages.error(
                    request, "Confirm Password didn't matched with Password!!!")
                return redirect('register')
        return render(request, "edge_register.html")
    else:
        return redirect("index")


def change_password(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            old_password = request.POST['old_password']
            new_password = request.POST['new_password']
            confirm_password = request.POST['confirm_password']

            if check_password(old_password, request.user.password):
                if confirm_password == new_password:
                    request.user.password = make_password(new_password)
                    request.user.save()
                    login(request, request.user)
                    messages.success(request, 'Password Updated Successfully')
                    return redirect('index')
                else:
                    messages.error(
                        request, "Confirm Password didn't matched with New Password!!!")
                    return redirect('change_password')
            else:
                messages.error(request, "You have entered wrong password!!!")
                return redirect('change_password')

        return render(request, "change_password.html")
    else:
        return redirect("loginview")


def update_profile(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            email = request.POST.get('email')
            contact = request.POST.get('contact')
            dob = request.POST.get('dob')
            gender = request.POST.get('gender')
            address = request.POST.get('address')
            pincode = request.POST.get('pincode')
            city = request.POST.get('city')
            state = request.POST.get('state')
            country = request.POST.get('country')

            if dob == "":
                dob = None
            else:
                dob = dob
            user_obj = User.objects.get(username=request.user)
            user_obj.first_name = first_name
            user_obj.last_name = last_name
            user_obj.email = email
            user_obj.contact = contact
            user_obj.dob = dob
            user_obj.gender = gender
            user_obj.save()

            try:
                add_obj = Address.objects.get(user=request.user)
            except:
                add_obj = Address.objects.create(user=request.user)

            add_obj.address = address
            add_obj.pincode = pincode
            add_obj.city = city
            add_obj.state = state
            add_obj.country = country
            add_obj.save()

            messages.success(request, 'Profile Updated')
            return redirect("update_profile")

        elif request.method == "GET":
            user_obj = User.objects.get(username=request.user)
            try:
                add_obj = Address.objects.get(user=request.user)
            except:
                add_obj = None
            return render(request, "update_profile.html", {"user_data": user_obj, "add_data": add_obj})
        else:
            return HttpResponse("Method Not Allowed!!!")
    else:
        return redirect("loginview")

def forgot_password(request):
    if request.method == "POST":
        username = request.POST['username']
        email = request.POST.get('email')
        contact = request.POST.get('contact')
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        
        if email or contact:
            if User.objects.filter(username = username).exists():
                user_obj = User.objects.get(username = username)

                if user_obj.email!=email or user_obj.contact_number!=contact:
                    if password==confirm_password:
                        user_obj.set_password(password)
                        user_obj.save()
                        login(request, user_obj)
                        return redirect('index')
                    else:
                        messages.error(request, "password and confirm password doesnot matched!")
                        return redirect('forgot_password')
                else:
                    messages.error(request, "Neither your email nor contact matched with saved data!")
                    return redirect('forgot_password')
                
            else:
                messages.error(request, "User not found with this username!")
                return redirect('forgot_password')
        else:
            messages.error(request, "contact or email is required!")
            return redirect('forgot_password')

        # if check_password(old_password, request.user.password):
        #     if confirm_password == new_password:
        #         request.user.password = make_password(new_password)
        #         request.user.save()
        #         login(request, request.user)
        #         messages.success(request, 'Password Updated Successfully')
        #         return redirect('index')
        #     else:
        #         messages.error(
        #             request, "Confirm Password didn't matched with New Password!!!")
        #         return redirect('change_password')
        # else:
        #     messages.error(request, "You have entered wrong password!!!")
        #     return redirect('change_password')

    return render(request, "edge_forgot_password.html")

def logoutview(request):
    if request.user.is_authenticated:
        logout(request)
        return redirect('loginview')
    return redirect('index')

def terms_condition(request):
    terms = terms_conditions.objects.first()
    return render(request, 'edge_terms_conditions.html', {"terms":terms})