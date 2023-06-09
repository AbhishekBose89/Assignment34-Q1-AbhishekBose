from urllib import request
from django.shortcuts import render
from django.views import View
from .serializers import ProductSerializer
from .cart import products
from django.http import JsonResponse, Http404
import json


# Create your views here.


# add product to cart
class CartView(View):
    def post(self, request):
        added_product = json.loads(request.body)
        added_product["product_id"] = len(products) + 1
        serialized_add_product = ProductSerializer(data=added_product)
        if serialized_add_product.is_valid():
            products.append(serialized_add_product.data)
            return JsonResponse(serialized_add_product.data, status=201)


# get search product from cart

# search by id
class SearchViewId(View):
    def get(self, request, product_id):
        found_product = None
        for product in products:
            if product["product_id"] == product_id:
                found_product = product
        if found_product:
            return JsonResponse(ProductSerializer(found_product).data, safe=False)
        else:
            raise Http404("Product not found")


# search by name
class SearchView(View):
    def get(self, request):
        query = request.GET.get("query")
        search_product = None
        for product in products:
            if product["name"] == query:
                search_product = product
        if search_product:
            return JsonResponse(ProductSerializer(search_product).data, safe=False)
        else:
            raise Http404("Product not found")


# get all products in cart
class MyCartView(View):
    def get(self, request):
        serialized_product = ProductSerializer(products, many=True).data
        return JsonResponse(serialized_product, safe=False)
     
# delete the product from cart
class CheckoutView(View):
    def delete(self,request,product_id):
        for product in products:
            if product["product_id"]== product_id:
                products.remove(product)
                return JsonResponse({"message": "Product is deleted"},status=200)
        return Http404("No product found to delete")    
            