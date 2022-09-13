from django.urls import path
from . import views

urlpatterns = [
    path('',views.order,name="order"),
    path('order-with-razorpay/',views.pay_razorpay,name="razorpay"),
    path('my-orders/',views.my_orders,name="my_orders"),
    
]