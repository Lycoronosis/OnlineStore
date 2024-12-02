from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import CustomUser, Product, ProductParameter, ProductImage, Order, OrderItem


# Register your models here.
class UserAdmin(BaseUserAdmin):
    model = CustomUser
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Additional Info', {'fields': ('phone_number', 'address')}),
    )
    list_display= ('username', 'email', 'phone_number', 'is_staff')
    search_fields = ('username', 'email', 'phonenumber')
    

class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price')
    list_editable = ('price',)
    fields = ('name', 'catalog_code', 'description', 'price')
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

class OrderItemInLine(admin.TabularInline):
    model = OrderItem
    extra = 0
    
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'created_at', 'is_paid')
    list_filter = ('is_paid', 'created_at')
    search_fields = ('user__username', 'phone_number')
    inlines = [OrderItemInLine]

admin.site.register(CustomUser, UserAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(ProductParameter)
admin.site.register(OrderItem)   
admin.site.register(Order, OrderAdmin)
admin.site.register(ProductImage, ProductImageAdmin)
