from django.http import Http404
from django.shortcuts import render

from rest_framework import viewsets
from core.models import Order,Product
from .serializers import ProductSerializer,OrderSerializer
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

#imports for the new branch
from rest_framework.views import APIView
from rest_framework.response import Response
from core.models import Product
from .serializers import *
from rest_framework import status
from rest_framework.decorators import api_view
from django.db.models import Q



class LatestProductList(APIView):
    # authentication_classes = [TokenAuthentication]
    # permission_classes = [IsAuthenticated]

    def get(self,request,format=None):
        products = Product.objects.all()[0:4]
        serializer = ProductSerializer(products,many=True)
        print(request.query_params)
        return Response(serializer.data)
    


class ProductDetail(APIView):
    def get_object(self, category_slug, product_slug):
        try:
            return Product.objects.filter(category_slug=category_slug).get(slug=product_slug)    
        except Product.DoesNotExist:
            raise status.HTTP_404_NOT_FOUND
        
    def get(self, request, category_slug, product_slug, format=None):
        product = self.get_object(category_slug,product_slug)    
        serializer = ProductSerializer(product)
        return Response(serializer.data)
    


class AddProcuctView(APIView):
    def post(self,request):
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)


class CategoryDetail(APIView):
    def get_object(self, category_slug):
        try:
            return Category.objects.get(slug=category_slug)
        except Category.DoesNotExist:
            raise Http404

    def get(self, request, category_slug, format=None):
        category = self.get_object(category_slug)    
        serializer = CategorySerializer(category)
        return Response(serializer.data)
    

@api_view
def search(request):
    query = request.data.get('query', '')    
    if query:
        products = Product.objects.filter(Q(name__icontains=query) | Q(description__icontains=query))
        serializer = ProductSerializer(products,many=True)
        return Response(serializer.data)
    return Response({"products":[]})