from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

from .models import Order, OrderItem, User


class OrderFrom(forms.Form):
    first_name = forms.CharField(max_length=50)
    last_name = forms.CharField(max_length=50)
    email = forms.EmailField()
    phone = forms.CharField(max_length=15)
    address = forms.CharField(widget=forms.Textarea)
    company_name = forms.CharField(max_length=100, required=False)
    tax_id = forms.CharField(max_length=15, required=False)
    
    def save(self, cart, user=None):
        order = Order.objects.create(
            user=user if user and user.is_authenticated else None,
            guest_email = self.cleaned_data['email'],
            guest_phone = self.cleaned_data['phone'],
            address = self.cleaned_data['address'],
        )
        for item in cart:
            OrderItem.objects.create(
                order=order,
                product=item['product'],
                quantity=item['quantity'],
            )
        return order
    
    def clean_phone(self):
        phone = self.cleaned_data['phone']
        if not phone.isdigit():
            raise forms.ValidationError("Please enter valid phone number")
        return phone
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        try:
            validate_email(email)
        except ValidationError:
            raise forms.ValidationError("Please enter valid email address.")


class GuestOrderSearchForm(forms.Form):
    guest_email = forms.EmailField(label="Enter your email to find your orders:")
    

class RegistrationFrom(UserCreationForm):
    email = forms.EmailField(required=True)
    phone_number = forms.CharField(max_length=15, required=False)
    address = forms.CharField(widget=forms.Textarea, required=False)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'phone_number', 'address', 'password1', 'password2']
        
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.phone_number = self.cleaned_data['phone_number']
        user.address = self.cleaned_data['address']
        if commit:
            user.save()
        return user
    

class LoginForm(AuthenticationForm):
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)
    