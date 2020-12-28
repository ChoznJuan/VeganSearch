from django.db import models
from django.core.validators import RegexValidator
from datetime import date
from datetime import datetime

# Create Products Class
class Product(models.Model):
    # Get Current Date
    dt = date.today()
    dtedit = dt.strftime("%m/%d/%Y")
    # upc codes are 12 chars ean codes can be 13 chars RegexValidator ensures only numbers in field
    upc = models.CharField(max_length=13, validators=[RegexValidator(r'^\d{1,13}$')])
    name = models.CharField(max_length=200)
    ingredients = models.TextField()
    vegan = models.BooleanField(default=False)
    source = models.CharField(max_length=200, default='n/a')

    
    def __str__(self):
        return f"{self.upc}, {self.name}"
    
    def ingredient_list(self):
        return self.ingredients.replace(',',';').split(';')
