from django import forms
from .models import Product

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'image', 'image_2', 'image_3', 'image_4', 'image_5']

class PaymentForm(forms.Form):
    amount = forms.DecimalField(label='Monto')
    card_holder = forms.CharField(label='Nombre del titular de la tarjeta')
    card_number = forms.CharField(label='Número de tarjeta')
    expiration_date = forms.CharField(label='Fecha de vencimiento (MM/YY)')
    cvc = forms.CharField(label='CVC')