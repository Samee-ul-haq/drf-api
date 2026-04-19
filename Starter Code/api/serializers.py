from rest_framework import serializers
from .models import Product, Order, OrderItem, User

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
    # This nests the full product details inside the order item
    product=ProductSerializer(read_only=True)
    class Meta:
        model=OrderItem
        fields=(
            'product',
            'quantity',
            'price',
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

class UserSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    username = serializers.CharField(max_length=150)
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user

class ProductInfoSerializer(serializers.Serializer):
    """ Get the list of all products, total count of products, 
     and the maximum price among the products by creating a 
     custom serializer that aggregates this information.
     The serializer should return a JSON response with the 
     following structure:API response structure:
     {
         "products": [ ... list of products ... ],
         "count": total_number_of_products,
         "max_price": maximum_price_among_products """    
    products=ProductSerializer(many=True)
    count=serializers.IntegerField()
    max_price=serializers.FloatField()

