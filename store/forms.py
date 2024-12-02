from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

from .models import Order, OrderItem, CustomUser, Product


from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from .models import Order, OrderItem

class OrderForm(forms.Form):
    first_name = forms.CharField(max_length=50, label="First Name")
    last_name = forms.CharField(max_length=50, label="Last Name")
    email = forms.EmailField(label="Email")
    phone = forms.CharField(max_length=15, label="Phone")
    country = forms.CharField(max_length=100, required=False, label="Country")
    city = forms.CharField(max_length=100, required=False, label="City")
    street = forms.CharField(max_length=255, required=False, label="Street")
    house_number = forms.CharField(max_length=50, required=False, label="House Number")
    zip_code = forms.CharField(max_length=20, required=False, label="ZIP Code")
    company_name = forms.CharField(max_length=100, required=False, label="Company Name")
    tax_id = forms.CharField(max_length=15, required=False, label="Tax ID")
    
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)  # Pobierz użytkownika z parametrów
        super().__init__(*args, **kwargs)
        if user and user.is_authenticated:
            # Automatyczne wypełnianie danych dla zalogowanego użytkownika
            self.fields['first_name'].initial = user.first_name
            self.fields['last_name'].initial = user.last_name
            self.fields['email'].initial = user.email
            self.fields['phone'].initial = user.phone_number
            self.fields['country'].initial = user.country
            self.fields['city'].initial = user.city
            self.fields['street'].initial = user.street
            self.fields['house_number'].initial = user.house_number
            self.fields['zip_code'].initial = user.zip_code

    def save(self, cart, user=None):
        # Tworzenie zamówienia
        order = Order.objects.create(
            user=user if user and user.is_authenticated else None,
            first_name=self.cleaned_data['first_name'],
            last_name=self.cleaned_data['last_name'],
            email=self.cleaned_data['email'],
            phone=self.cleaned_data['phone'],
            country=self.cleaned_data['country'],
            city=self.cleaned_data['city'],
            street=self.cleaned_data['street'],
            house_number=self.cleaned_data['house_number'],
            zip_code=self.cleaned_data['zip_code'],
            company_name=self.cleaned_data['company_name'],
            tax_id=self.cleaned_data['tax_id'],
        )
        # Dodawanie produktów do zamówienia
        for item_id, item_data in cart.items():
            product = Product.objects.get(id=item_id)
            OrderItem.objects.create(
                order=order,
                product=product,
                quantity=item_data['quantity'],
                price=item_data['price'],
            )
        return order

    def clean_phone(self):
        phone = self.cleaned_data['phone']
        if not phone.isdigit():
            raise forms.ValidationError("Please enter a valid phone number")
        return phone

    def clean_email(self):
        email = self.cleaned_data.get('email')
        try:
            validate_email(email)
        except ValidationError:
            raise forms.ValidationError("Please enter a valid email address.")
        return email



class GuestOrderSearchForm(forms.Form):
    guest_email = forms.EmailField(label="Enter your email to find your orders:")
    

class RegistrationForm(UserCreationForm):
    email = forms.EmailField(
        required=True, 
        widget=forms.EmailInput(attrs={'placeholder': 'Email address'})
    )
    phone_number = forms.CharField(
        max_length=15, 
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'Phone number (optional)'})
    )
    country = forms.CharField(
        max_length=100, 
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'Country (optional)'})
    )
    city = forms.CharField(
        max_length=100, 
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'City (optional)'})
    )
    street = forms.CharField(
        max_length=255, 
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'Street name (optional)'})
    )
    house_number = forms.CharField(
        max_length=10, 
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'House/Apartment number (optional)'})
    )
    zip_code = forms.CharField(
        max_length=20, 
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'Zip Code (optional)'})
    )

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'phone_number', 'country', 'city', 'street', 'house_number', 'zip_code', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.phone_number = self.cleaned_data.get('phone_number')
        user.country = self.cleaned_data.get('country')
        user.city = self.cleaned_data.get('city')
        user.street = self.cleaned_data.get('street')
        user.house_number = self.cleaned_data.get('house_number')
        user.zip_code = self.cleaned_data.get('zip_code')
        if commit:
            user.save()
        return user

    

class LoginForm(forms.Form):
        
    username = forms.CharField(
        max_length=150,
        label = "Username",
        widget=forms.TextInput(attrs={'placeholder': 'Enter username'}),
        )
    password = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={'placeholder': 'Enter password'}),
        )
    remember_me = forms.BooleanField(required=False, widget=forms.CheckboxInput())
    
