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

class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model=OrderItem
        fields=(
            'product',
            'quantity',
        )

class OrderSerializer(serializers.ModelSerializer):
    items=OrderItemSerializer(many=True,read_only=True)
    total_price=serializers.SerializerMethodField()

    def get_total_price(self,obj):
        order_items=obj.items.all()
        return sum(order_item.item_subtotal for order_item in order_items)
    
    class Meta:
        model=Order
        fields=(
            'order_id',
            'created_at',
            'user',
            'status',
            "total_price",
            'items',
        )

class ProductInfoSerializer(serializers.Serializer):
    # Get the list of all products, total count of products, 
    # and the maximum price among the products by creating a 
    # custom serializer that aggregates this information.
    # The serializer should return a JSON response with the 
    # following structure:API response structure:
    # {
    #     "products": [ ... list of products ... ],
    #     "count": total_number_of_products,
    #     "max_price": maximum_price_among_products     
    products=ProductSerializer(many=True)
    count=serializers.IntegerField()
    max_price=serializers.FloatField()