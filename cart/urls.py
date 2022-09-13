from django.urls import path
from . import views

urlpatterns = [
    path('my-cart/',views.cart,name="cart"),
    # path('proceed-to-order/',views.proceed_to_order,name="proceed_to_order"),
    path('add_cart/<int:product_id>/',views.add_cart,name="add_cart"),
    path('IncQuntity/<int:val>/<int:id>/',views.IncQuntity,name="IncQuntity"),
    path('remove_cart_item/<int:product_id>/<int:cart_item_id>/',views.remove_cart_item,name="remove_cart_item")
]