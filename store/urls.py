from django.urls import path
from . import views


urlpatterns = [
    path('', views.landing_page, name="landing_page"),
    path('products/', views.product_list, name= 'product_list'),
    path('products/<int:product_id>/', views.product_detail, name='product_detail'),
    path('cart/', views.cart_detail, name="cart_detail"),
    path('cart/add/<int:product_id>/', views.cart_add, name="cart_add"),
    path('cart/remove/<int:product_id>/', views.cart_remove, name="cart_remove"),
    path('checkout/', views.checkout, name='checkout')
]