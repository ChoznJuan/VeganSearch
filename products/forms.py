from django import forms
from .models import Contacts
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from .models import no_past


class ProductForm(forms.ModelForm):
    upc = forms.CharField(label='', widget=forms.TextInput(
    attrs={"placeholder":"UPC Code"}))
    name = forms.CharField(label='', widget=forms.TextInput(
    attrs={"placeholder":"Product Name"}))
    ingredients = forms.CharField(label='', widget=forms.Textarea(
    attrs={"placeholder":"Product Ingredients"}))
    vegan = forms.BooleanField(label='Vegan', widget=forms.RadioSelect(choices=[(True, 'Yes'),(False,'No')]))
    source = forms.CharField(label='', widget=forms.TextInput(attrs={"placeholder":"Source Of Information"})}))
   
    class Meta:
        model = Product
        fields = [
            'upc', 
            'name',
            'ingredients',
            'vegan',
            'source'
        ]
            
