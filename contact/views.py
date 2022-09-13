from django.shortcuts import redirect, render
from .models import *

# Create your views here.

def contact_form(request):
    if request.method == "POST":
        print(request)
        name = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone']
        subject = request.POST['subject']
        message = request.POST['message']
        
        contact.objects.create(name=name, email=email, phone=phone, subject=subject, message=message)
        return redirect("contact_form")
        
    return render(request,"contact.html")
