from django.shortcuts import render
from .models import Product
from django.http import HttpResponse
import json
from django.db.models import Q
import requests
from dotenv import load_dotenv
import os

load_dotenv()

# UPC Web API Lookup
def upc_lookup(query):
    url = "https://nutritionix-api.p.rapidapi.com/v1_1/item"
    querystring = {"upc": query}
    headers = {
        # rapidapi key is privatized
        'x-rapidapi-key': str(os.getenv('x_rapidapi_key')),
        'x-rapidapi-host': "nutritionix-api.p.rapidapi.com"
        }
    response = requests.request("GET", url, headers=headers, params=querystring)
    query_json = json.loads(response.text)
    api = dict()
    api['ingredients'] = query_json['nf_ingredient_statement']
    api['name'] = query_json['item_name']
    return api

def name_lookup(query):
    search = query
    api_key = os.getenv('gov_api')
    url = "https://api.nal.usda.gov/fdc/v1/foods/search?api_key="
    query = str(url)+api_key+"&q="+str(search)+"&brandOwner="+str(search) + "&pageNumber=1&pageSize=10&application/json" 
    response = requests.request("GET",query)
    query_json = json.loads(response.text)
    return(query_json)

# Product Name View
def product_detail_view_name(request):
    query=None
    if request.method == 'GET':
        query = request.GET.get('prod')
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
                try:
                    obj = upc_lookup(query)
                    context ={
                        'Name' : obj['name'],
                        'Ingredients_List' : obj['ingredients'].replace(',',';').split(';'),
                        'UPC' : query
                    }
                    u = Product(name=obj['name'], ingredients=obj['ingredients'], upc=query)
                    u.save()
                    # print(str(obj['name']) + " successfully added to database" )
                    return render(request, "product/detail.html", context)
                except:        
                    try:
                        obj = name_lookup(query)
                        i = 0
                        api = {}
                        for prod in obj['foods']:
                            prod.pop('foodNutrients')
                            api [i] = {
                                'Name' : str(prod['brandOwner']) + "-" + str(prod['description']),
                                'Ingredients_List' : prod['ingredients'],
                                'UPC' : prod['gtinUpc']
                            }
                            i = i + 1
                            u = Product(name=str(prod['brandOwner']) + "-" + str(prod['description']), ingredients=prod['ingredients'], upc=prod['gtinUpc'])
                            u.save()
                            # print(str(prod['brandOwner']) + "-" + str(prod['description']) + " was successfully added to database.")
                        return render(request, "product/upc_detail.html", {"api": api.items()})
                    except:
                        context ={
                        'Name' : query
                        }
                        return render(request, "product/not_found.html",context)