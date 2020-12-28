from django.urls import path
from .views import product_detail_view_name

urlpatterns = [
    path('details',product_detail_view_name,name="details"),
]