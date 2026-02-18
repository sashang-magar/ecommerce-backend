from rest_framework import serializers
from store.models import Product , Collection
from decimal import Decimal

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


    

 