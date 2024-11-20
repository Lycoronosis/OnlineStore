from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, Http404

from .models import Product
from .utils import Cart
from .forms import OrderFrom

# Create your views here.

def landing_page(request):
    return render(request, 'landing_page.html')


def product_list(request):
    products = Product.objects.all()
    return render(request, 'product_list.html', {'products': products})


def product_detail(request, product_id):
    try:
        product = Product.objects.get(id=product_id)
    except Product.DoesNotExist:
        raise Http404("Product not found")
    return render(request, 'product_detail.html', {'product': product})


def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.add(product=product)
    return redirect('cart_detail.html')

def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product=product)
    return redirect('cart_detail.html')

def cart_detail(request):
    cart = Cart(request)
    return render(request, 'cart_detail.html', {'cart': cart})

def checkout(request):
    cart = Cart(request)
    if request.method == 'POST':
        form = OrderFrom(request.POST)
        if form.is_valid():
            cart.clear()
            return redirect('order_complete')
    else:
        form = OrderFrom()
    return render(request, 'checkout.html', {'form': form, 'cart': cart})