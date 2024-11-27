from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Product, ProductParameter, ProductImage, Order, OrderItem


# Register your models here.
class UserAdmin(BaseUserAdmin):
    model = User
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Additional Info', {'fields': ('phone_number', 'address', 'is_admin')}),
    )
    list_display= ('username', 'email', 'phone_number', 'is_staff', 'is_admin')
    search_fields = ('username', 'email', 'phonenumber')
    

class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price')
    list_editable = ('price',)
    fields = ('name', 'description', 'price')
    search_fields = ('name',)
    list_filter = ('price',)

    def save_model(self, request, obj, form, change):
        if not obj.catalog_code:
            obj.catalog_code = f'CAT-{obj.id}'
        super().save_model(request, obj, form, change)


class ProductImageAdmin(admin.ModelAdmin):
    list_display = ('product', 'image')
    search_fields = ('product__name',)
    list_filter = ('product',)


class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'guest_email', 'created_at', 'is_paid')
    list_filter = ('is_paid', 'created_at')
    search_fields = ('user__username', 'guest_email', 'guest_phone')
    inlines = []


class OrderItemInLine(admin.TabularInline):
    model = OrderItem
    extra = 0
    

class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'guest_email', 'created_at', 'is_paid')
    inlines = [OrderItemInLine]
 
 
admin.site.register(User, UserAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(ProductParameter)
admin.site.register(OrderItem)   
admin.site.register(Order, OrderAdmin)
admin.site.register(ProductImage, ProductImageAdmin)
