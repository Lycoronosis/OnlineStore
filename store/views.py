from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, Http404, JsonResponse
from django.db.models import Sum, F, Q
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, logout, get_backends
from django.conf import settings
from django.contrib.sessions.models import Session



from .models import Product, Order, OrderItem
from .utils import Cart
from .forms import OrderForm, GuestOrderSearchForm, RegistrationForm, LoginForm

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
    quantity = int(request.POST.get('quantity', 1))
    cart.add(product=product, quantity=1)
    messages.success(request, f'{product.name} has been added to your cart.')
    return redirect('product_detail', product_id=product.id)

def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    return redirect('cart_detail')

def cart_detail(request):
    cart = Cart(request)
    return render(request, 'cart_detail.html', {'cart': cart})

@login_required
def checkout(request):
    cart = request.session.get('cart', {})
    print("Cart content:", cart)
    if request.method == 'POST':
        form = OrderForm(request.POST, user=request.user)
        if form.is_valid():
            order = form.save(cart=cart, user=request.user)
            return redirect('order_complete', order_id=order.id)
    else:
        form = OrderForm(user=request.user)
    
    return render(request, 'checkout.html', {'form': form})

def order_complete(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    total_price = sum(item.get_total_price() for item in order.items.all())

    return render(request, 'order_complete.html', {
        'order': order,
        'total_price': total_price
    })
    
@login_required
def order_list(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'order_list.html', {'orders': orders})

@login_required
def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'order_detail.html', {'order': order})

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Your account has been created and you are logged in.")
            return redirect('landing_page')
        else:
            messages.error(request, "Please correct the errors below")
    else:
        form = RegistrationForm()
    return render(request, 'register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        print(form.errors)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, "Login successful!")
                return redirect('landing_page')
            else:
                messages.error(request, "Invalid username or password. Please try again.")
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})



def logout_view(request):
    logout(request)
    request.session.flush()
    messages.success(request, "You are logged out.")
    return redirect('landing_page')
