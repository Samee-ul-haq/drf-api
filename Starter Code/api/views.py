from django.shortcuts import get_object_or_404
from api.serializers import ProductSerializer,OrderSerializer,OrderItemSerializer,ProductInfoSerialize
from api.models import Product,Order,OrderItem
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.db.models import Max
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.permissions import (
    IsAuthenticated,
    IsAdminUser,
    AllowAny
)
from api.filters import ProductFilter,InStockFilterBackend
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.pagination import PageNumberPagination

class ProductListCreateAPIView(generics.ListCreateAPIView):
    queryset=Product.objects.all()
    serializer_class=ProductSerializer
    filterset_class=ProductFilter
    filter_backends=[
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
        InStockFilterBackend,
        ]
    search_fields=['name','description']
    ordering_fields=['name','price','stock']
    pagination_class=PageNumberPagination
    pagination_class.page_query_param='pagenum'
    pagination_class.page_size_query_param='size'
    pagination_class.max_page_size=10

    def get_permission(self):
        self.permission_class=[AllowAny]
        if self.request.method=='POST':
            self.permission_class=[IsAdminUser]
        return super().get_permission()

# class ProductCreateAPIView(generics.CreateAPIView):
#     model=Product
#     serializer_class =ProductSerializer

# @api_view(['GET'])
# def product_list(request):
#     products=Product.objects.all()
#     serializer=ProductSerializer(products,many=True)
#     return Response(serializer.data)

# @api_view(['GET'])
# def product_detail(request,pk):
#     product=get_object_or_404(Product,pk=pk)
#     serializer=ProductSerializer(product)
#     return Response(serializer.data)

class ProductDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset=Product.objects.all()
    serializer_class=ProductSerializer
    lookup_url_kwarg='product_id'

@api_view(['GET'])
def order_list(request):
    order=Order.objects.all()
    serializer=OrderSerializer(order,many=True)
    return Response(serializer.data)

@api_view(['GET'])
def orderItem_list(request):
    order_item=OrderItem.objects.all()
    serializer=OrderItemSerializer(order_item,many=True)
    return Response(serializer.data)

@api_view(['GET'])
def product_info(request):
    products=Product.objects.all()
    serializer=ProductInfoSerialize({
        'products':products,
        'count':len(products), 
        'max_price':products.aggregate(max_price=Max('price'))['max_price']
    })
    return Response(serializer.data)

# class UserCreateApi():


class productInfoView(APIView):
    def get(sef,request):
        products=Product.objects.all()
        serializer=ProductInfoSerialize({
            'products':products,
            'count':len(products), 
            'max_price':products.aggregate(max_price=Max('price'))['max_price']
        })
        return Response(serializer.data)