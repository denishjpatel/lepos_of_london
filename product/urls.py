from django.urls import path
from . import views

urlpatterns = [
    path('',views.index,name="index"),
    path('products/',views.products,name="products"),
    path('products/<int:id>',views.product_details,name="product_details"),
    path('about/',views.about,name="about"),
    path('wishlist/',views.show_wishlist,name="wishlist"),
    path('add_wishlist/',views.add_wishlist,name="add_wishlist"),
]