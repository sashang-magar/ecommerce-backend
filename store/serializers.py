from itertools import product
from rest_framework import serializers
from store.models import CartItem, Product , Collection , Review , Cart
from decimal import Decimal

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['id' , 'date' , 'name' , 'description']

    def create(self, validated_data):
        product_id = self.context['product_id']
        return Review.objects.create(product_id=product_id, **validated_data)
    


class CollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collection
        fields = ['id' , 'title', 'products_count']
    
    products_count = serializers.IntegerField(read_only=True)


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'title' , 'description', 'slug', 'inventory' , 'unit_price' , 'price_with_tax' , 'collection']

    price_with_tax = serializers.SerializerMethodField(method_name='calculate_tax')
    def calculate_tax(self , product : Product ):
        return product.unit_price * Decimal(1.1)
    
class SimpleProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product 
        fields = ['id' , 'title' , 'unit_price' ]
class CartItemSerializer(serializers.ModelSerializer):
    product = SimpleProductSerializer(read_only=True)
    total_price = serializers.SerializerMethodField()

    def get_total_price(self , cart_item:CartItem):
        return cart_item.quantity * cart_item.product.unit_price
    class Meta:
        model =CartItem     
        fields = ['id' , 'product' , 'quantity','total_price']   

class AddCartItemSerializer(serializers.ModelSerializer):
    product_id = serializers.IntegerField()

    def validate_product_id(self , value):
        if not Product.objects.filter(pk=value).exists():
            raise serializers.ValidationError('no product of given id is found')
        return value


    def save(self , **kwargs):
        cart_id = self.context['cart_id']
        product_id=self.validated_data['product_id']
        quantity = self.validated_data['quantity']
        try:
            cart_item=CartItem.objects.get(cart_id=cart_id , product_id=product_id)
            cart_item.quantity += quantity
            cart_item.save()
            self.instance = cart_item
        except CartItem.DoesNotExist:
            self.instance=CartItem.objects.create(cart_id=cart_id , **self.validated_data)
        
        return self.instance
        
    class Meta:
        model = CartItem   
        fields = ['id' , 'product_id' , 'quantity']    

class UpdateCartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ['quantity']
class CartSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only = True)
    items = CartItemSerializer(many = True, read_only=True)
    total_price = serializers.SerializerMethodField()

    def get_total_price(self , cart):
        return sum([item.quantity * item.product.unit_price for item in cart.items.all()])
    class Meta:
        model = Cart    
        fields = ['id', 'items', 'total_price' ]

       
    #for validating User registration
    # def validate(self, data):
    #     if data['password']!= data['confirm_password']:
    #         return serializers.ValidationError('password do not match')
    #     return data

    # id = serializers.IntegerField()
    # title = serializers.CharField(max_length=255)
    # price = serializers.DecimalField(max_digits=6 , decimal_places=2 , source='unit_price')
    
    
    #Four way to serialize
   #1st primary key integer
    # collection = serializers.PrimaryKeyRelatedField(
    #     queryset = Collection.objects.all()
    # )

    #2nd String
    # collection = serializers.StringRelatedField()

    #3rd value pair , collection render as object(nested object)
    # collection = CollectionSerializer()

    #4th creating hyperlink
    # collection = serializers.HyperlinkedRelatedField(
    #     queryset = Collection.objects.all(),
    #     view_name = 'collection-detail'
    # )


    

 