from .utils import Cart

class CartMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        
    def __call__(self, request):
        cart = Cart(request)
        request.cart = cart
        response = self.get_response(request)
        return response