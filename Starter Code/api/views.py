from django.shortcuts import get_object_or_404
from rest_framework import permissions
from api.serializers import ProductSerializer,OrderSerializer,OrderItemSerializer,ProductInfoSerializer
from api.models import Product,Order,OrderItem
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.db.models import Max,Sum,F
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.permissions import (
    IsAuthenticated,
    IsAdminUser,
    AllowAny,
)
from django.contrib.auth.models import get_user_model # to get the user model, which is useful if you have a custom user model
from api.filters import ProductFilter,InStockFilterBackend
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.pagination import PageNumberPagination
from project1.start.serializers import UserSerializer
from rest_framework import viewsets

class StandardResultsSetPagination(PageNumberPagination):
    page_query_param = 'pagenum'
    page_size_query_param = 'size'
    max_page_size = 10

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
    pagination_class=StandardResultsSetPagination
    

    def get_permissions(self):
        if self.request.method == 'GET':
            self.permission_classes = [IsAuthenticated]
        else:
            self.permission_classes = [IsAdminUser]
        return super().get_permissions()

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

# @api_view(['GET'])
# def order_list(request):
#     order=Order.objects.all()
#     serializer=OrderSerializer(order,many=True)
#     return Response(serializer.data)

# @api_view(['GET'])
# def orderItem_list(request):
#     order_item=OrderItem.objects.all()
#     serializer=OrderItemSerializer(order_item,many=True)
#     return Response(serializer.data)

class orderList(generics.ListAPIView):
    permission_classes=[IsAuthenticated]
    queryset=Order.objects.all()
    serializer_class=OrderSerializer 
    

class orderItemList(generics.ListAPIView):
    permission_classes=[IsAuthenticated]
    queryset=OrderItem.objects.all()
    serializer_class=OrderItemSerializer # to serialize the order items and return them in the response


@api_view(['GET'])
def product_info(request):
    # prefetch_related to optimize the query and avoid N+1 problem when 
    # accessing related data in the serializer for each product.
    # It will fetch all related order items and their associated products in a single query, 
    # improving performance when serializing the product information.
    products=Product.objects.prefetch_related('items','items__product').all()
    serializer=ProductInfoSerializer({
        'products':products,
        'count':len(products), 
        'max_price':products.aggregate(max_price=Max('price'))['max_price']
    })
    return Response(serializer.data)



class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # 1. Use prefetch_related to grab all OrderItems in ONE extra query
        # 2. Use annotate to calculate the total price in the Database, not Python
        return Order.objects.filter(user=self.request.user).prefetch_related(
            'items__product'
        ).annotate(
            total_price=Sum(F('items__quantity') * F('items__price'))
        )

class productInfoView(APIView):
    permission_classes=[IsAuthenticated]
    def get(self,request):
        products=Product.objects.all()
        serializer=ProductInfoSerializer({
            'products':products,
            'count':len(products), 
            'max_price':products.aggregate(max_price=Max('price'))['max_price']
        })
        return Response(serializer.data)
    

class RegisterView(generics.CreateAPIView):
    queryset=get_user_model().objects.all()
    # Make sure to create a UserSerializer that handles user registration, including password hashing and validation.
    # UserSerializer should include fields like username, email, and password, and should implement the create method to handle user creation properly.
    serializer_class=UserSerializer 
    permission_classes=[AllowAny]



class ProductViewSet(viewsets.ModelViewSet):
    permission_classes=[IsAuthenticated]
    queryset = Product.objects.all()
    serializer_class = ProductSerializer