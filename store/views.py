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
from .forms import OrderFrom, GuestOrderSearchForm, RegistrationFrom, LoginForm

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

def checkout(request):
    cart = Cart(request)
    if len(cart) == 0:
        messages.error(request, "Your cart is empty. Add items to proceed.")
        return redirect('cart_detail')
    if request.method == 'POST':
        form = OrderFrom(request.POST)
        if form.is_valid():
            if request.user.is_authenticated:
                order = Order.objects.create(
                    user = request.user,
                    address = form.cleaned_data['address'],
                )
            else:
                order = Order.objects.create(
                    guest_email = form.cleaned_data['email'],
                    guest_phone = form.cleaned_data['phone'],
                    address = form.cleaned_data['address'],
                )
            for item in cart:
                OrderItem.objects.create(
                    order=order,
                    product=item['product'],
                    quantity=item['quantity'],
                )
            cart.clear()
            return redirect('order_complete', order_id=order.id)
        else:
            messages.error(request, "Please correct errors in form")
            
    else:
        form = OrderFrom()
    return render(request, 'checkout.html', {'form': form, 'cart': cart})

def order_complete(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    total_price = order.items.aggregate(
        total=Sum(F('product__price') * F('quantity'))
    )['total'] or 0
    return render(request, 'order_complete.html', {
        'order': order,
        'total_price': total_price
        })
    
def order_list(request):
    form = GuestOrderSearchForm()
    orders = None
        
    if request.user.is_authenticated:
        orders = (
            Order.objects.filter(user=request.user)
            .annotate(total_price=Sum(F('items__product__price') * F('items__quantity')))
            .order_by('-created_at')
        )
    elif request.method == 'POST':
        form = GuestOrderSearchForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['guest_email']
            orders = (
                Order.objects.filter(guest_email=email)
                .annotate(total_price=Sum(F('items__product__price') * F('items__quantity')))
                .order_by('-created_at')
            )
            if not orders.exists():
                messages.error(request, "No orders found for this email.")
        else:
            messages.error(request, "Invalid email address.")

    return render(request, 'order_list.html', {'orders': orders, 'form': form})

def register(request):
    if request.method == 'POST':
        form = RegistrationFrom(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Your account has been created and you are logged in.")
            return redirect('landing_page')
        else:
            messages.error(request, "Please correct the errors below")
    else:
        form = RegistrationFrom()
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
