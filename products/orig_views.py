from django.shortcuts import render
from .models import Product
from django.http import HttpResponse
import json
from django.db.models import Q
import requests
from dotenv import load_dotenv

load_dotenv()

# UPC Web API Lookup
def upc_lookup(query):
    url = "https://nutritionix-api.p.rapidapi.com/v1_1/item"
    querystring = {"upc": query}
    headers = {
        # rapidapi key is privatized
        'x-rapidapi-key': 'F3i9V4rEe9mshgjqpuSNb2QztX6jp11SnE6jsnNoM3D2iL4GdV',
        'x-rapidapi-host': "nutritionix-api.p.rapidapi.com"
        }
    response = requests.request("GET", url, headers=headers, params=querystring)
    query_json = json.loads(response.text)
    ingredients = query_json['nf_ingredient_statement']
    name = query_json['item_name']

# Product Name View
def product_detail_view_name(request):
    query=None
    if request.method == 'GET':
        query = request.GET.get('prod')
        print(query)
        try:
            obj = Product.objects.get(name__icontains=query)
            context ={
                'Name' : obj.name,
                'UPC' : obj.upc,
                'Ingredients_List' : obj.ingredients.replace(',',';').split(';'),
                'Vegan' : obj.vegan
            }
            return render(request, "product/detail.html", context)
        except:
            try:
                obj = Product.objects.get(upc__icontains=query)
                context ={
                    'Name' : obj.name,
                    'UPC' : obj.upc,
                    'Ingredients_List' : obj.ingredients.replace(',',';').split(';'),
                    'Vegan' : obj.vegan
                }
                return render(request, "product/detail.html", context)
            except:
                context ={
                    'Name' : query
                }
                return render(request, "product/not_found.html",context)
            
