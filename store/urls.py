from django.contrib.auth import views as auth_views
from django.urls import path, include
from . import views


urlpatterns = [
    path('', views.landing_page, name="landing_page"),
    path('products/', views.product_list, name= 'product_list'),
    path('products/<int:product_id>/', views.product_detail, name='product_detail'),
    path('cart/', views.cart_detail, name="cart_detail"),
    path('cart/add/<int:product_id>/', views.cart_add, name="cart_add"),
    path('cart/remove/<int:product_id>/', views.cart_remove, name="cart_remove"),
    path('checkout/', views.checkout, name='checkout'),
    path('order/complete/<int:order_id>', views.order_complete, name='order_complete'),
    path('order_list/', views.order_list, name = 'order_list'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.landing_page, name='logout'),
    path('gallery/', views.landing_page, name='gallery'),
    path('downloads/', views.landing_page, name='downloads'),
    path('contact/', views.landing_page, name='contact'),
    path('accounts/', include('allauth.urls')),
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset_done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset_done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    ]