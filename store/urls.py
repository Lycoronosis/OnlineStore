from django.urls import path
from . import views


urlpatterns = [
    path('', views.landing_page, name="landing_page"),
    path('products/', views.product_list, name= 'product_list'),
    path('products/<int:product_id>/', views.product_detail, name='product_detail')
]