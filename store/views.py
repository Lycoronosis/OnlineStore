from django.shortcuts import render
from django.http import HttpResponse, Http404

from .models import Product

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
