from django import forms


class OrderFrom(forms.Form):
    first_name = forms.CharField(max_length=50)
    last_name = forms.CharField(max_length=50)
    email = forms.EmailField()
    phone = forms.CharField(max_length=15)
    address = forms.CharField(widget=forms.Textarea)
    company_name = forms.CharField(max_length=100, required=False)
    tax_id = forms.CharField(max_length=15, required=False)
    
