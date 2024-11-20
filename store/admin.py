from django.contrib import admin
from .models import User, Product, ProductParameter, ProductImage, Order, OrderItem

# Register your models here.
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price')
    list_editable = ('price',)
    fields = ('name', 'description', 'price')
    search_fields = ('name',)


admin.site.register(User)
admin.site.register(Product, ProductAdmin)
admin.site.register(ProductParameter)
admin.site.register(ProductImage)
admin.site.register(Order)
admin.site.register(OrderItem)
