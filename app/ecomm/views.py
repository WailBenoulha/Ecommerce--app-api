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


# class ProductViewSet(viewsets.ModelViewSet):
#     serializer_class = ProductSerializer
#     queryset = Product.objects.all()
#     authentication_classes = [TokenAuthentication]
#     permission_classes = [IsAuthenticated]

#     def perform_create(self, serializer):
#         return serializer.save(create_by=self.request.user)

class LatestProductList(APIView):
    # authentication_classes = [TokenAuthentication]
    # permission_classes = [IsAuthenticated]

    def get(self,request,format=None):
        products = Product.objects.all()[0:4]
        serializer = ProductSerializer(products,many=True)
        return Response(serializer.data)
    
    def post(self,request, *args, **kwargs):
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid:
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    queryset = Order.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]


class CategoryView(APIView):
    def get(self,request,format=None):
        category = Category.objects.all()    
        serializer = CategorySerializer(category,many=True)
        return Response(serializer.data)
    