from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete


# Create your models here.

# Model for generic user
class User(AbstractUser):
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    is_admin = models.BooleanField(default=False)

    class Meta:
        permissions = [
            ("can_view_product", "Can view product")
        ]
        

# Model for products on website
class Product(models.Model):
    name = models.CharField(max_length=255)
    catalog_code = models.CharField(max_length=50, unique=True)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    is_active = models.BooleanField(default=True)


    def __str__(self):
        return self.name
    

# Model for products parameters to add later through form
class ProductParameter(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='parameters')
    key = models.CharField(max_length=100)
    value = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.key}: {self.value}"
    

# Function for uploading images to product folder
def product_image_upload_path(instance, filename):
    return f"products/{instance.product.id}/images/{filename}"


# Model for product images
class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name= 'images')
    image = models.ImageField(upload_to= product_image_upload_path)
    is_main = models.BooleanField(default=False)

    def __str__(self):
        return f"Image for {self.product.name}"
    
    def get_main_image(self):
        return self.images.filter(is_main=True).first()
    

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    guest_email = models.EmailField(null=True, blank=True)
    guest_phone = models.CharField(max_length=15, null=True, blank=True)
    address = models.TextField()
    is_paid = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order {self.id} - {self.user.username if self.user else 'Guest'}"
    
    # def get_total_price(self):
    #     return self.items.aggregate(total=Sum(F('product__price') * F('quantity')))['total'] or 0
    

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    def get_total_price(self):
        return self.product.price * self.quantity
    
    def __str__(self):
        return f"{self.get_total_price}"
    
    def clean(self):
        if self.quantity <= 0:
            raise ValidationError("Quantity must be greater than 0.")
    

class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    
    def __str__(self):
        return f"{self.product.name} x {self.quantity}"
    
    def get_total_price(self):
        return self.product.price * self.quantity
    
    @receiver(post_save, sender=OrderItem)
    def clean_cart_after_order(sender, instance, **kwargs):
        if instance.order.user:
            CartItem.objects.filter(user=instance.order.user).delete()

    
    
