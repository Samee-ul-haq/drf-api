from rest_framework import serializers
from .models import Product,Order,OrderItem
from django.contrib.auth.models import User

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model=Product
        fields=(
            'description',
            'name',
            'price',
            'stock',
        )

    def validate_price(self,value):
        if value<=0:
            raise serializers.ValidationError(
                "Price can not be -ve"
            )
        return value

class OrderSerializer(serializers.ModelSerializer):
   # items=OrderItemSerializer(many=True,read_only=True)
    class Meta:
        model=Order
        fields=(
            'order_id',
            'created_at',
            'user',
            'status',
        )

class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model=OrderItem
        fields=(
            'product',
            'quantity',
        )

class ProductInfoSerialize(serializers.Serializer):
    products=ProductSerializer(many=True)
    count=serializers.IntegerField()
    max_price=serializers.FloatField()