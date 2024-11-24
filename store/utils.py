
from .models import Product

class Cart:
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get('cart')
        if not cart:
            cart = self.session['cart'] = {}
        self.cart = cart
        
    def __len__(self):
        return sum(item['quantity'] for item in self.cart.values())
        
    def add(self, product, quantity=1):
        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {'quantity': quantity, 'price':float(product.price)}
        else:
            self.cart[product_id]['quantity'] += quantity
        self.save()
        
    def save(self):
        self.session.modified = True
        
    def remove(self, product):
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()
            
    def clear(self):
        self.session['cart'] = {}
        self.save()
        
    def __iter__(self):
        products_ids = self.cart.keys()
        products = Product.objects.filter(id__in=products_ids)
        for product in products:
            cart_item = self.cart[str(product.id)]
            cart_item['product'] = product
            cart_item['total_price'] = float(cart_item['price']) * cart_item['quantity']
            yield cart_item
            
    def get_total_price(self):
        return sum(
            float(item['price']) * item['quantity']
            for item in self.cart.values()
        )
        
    def is_empty(self):
        return len(self.cart) == 0
    