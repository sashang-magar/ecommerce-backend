from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import OrderItem, Product , Collection , Review
from .serializers import ProductSerializer , CollectionSerializer , ReviewSerializer
from rest_framework import status
from django.db.models import Count
from rest_framework.views import APIView
from rest_framework.mixins import ListModelMixin, CreateModelMixin
from rest_framework.generics import ListCreateAPIView , RetrieveUpdateDestroyAPIView
from rest_framework.viewsets import ModelViewSet
from django_filters.rest_framework import DjangoFilterBackend


class ReviewViewSet(ModelViewSet):
    # queryset = Review.objects.all() # Would return ALL reviews
    serializer_class = ReviewSerializer

    def get_queryset(self):
        return Review.objects.filter(product_id=self.kwargs['product_pk'])

    def get_serializer_context(self):
        return {'product_id':self.kwargs['product_pk'] }
    
#ModelViewSet
class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class =ProductSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['collection_id']

    #instead of filter we use filter backend
    # def get_queryset(self):
    #     queryset = Product.objects.all()
    #     collection_id = self.request.query_params.get('collection_id')
    #     if collection_id is not None:
    #         queryset = queryset.filter(collection_id=collection_id)
    #     return queryset

    def get_serializer_context(self):
        return {'request':self.request}
    def destroy(self, request, *args, **kwargs):
        if OrderItem.objects.filter(product_id=kwargs['pk']).exists():
            return Response({'error':'product cannot be deleted as it is associated with OrderItem'},status=status.HTTP_405_METHOD_NOT_ALLOWED)
        return super().destroy(request, *args, **kwargs)

class CollectionViewSet(ModelViewSet):
    queryset = Collection.objects.annotate(products_count = Count('products')).all()
    serializer_class = CollectionSerializer
    
    def destroy(self, request, *args, **kwargs):
        if Product.objects.filter(collection_id=kwargs['pk']).count() > 0: #use exists instead count
            return Response({'error':'collection cannot be deleted as associated with product' }, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        return super().destroy(request, *args, **kwargs)
    




#Generic View
# class ProductList(ListCreateAPIView):
#     queryset = Product.objects.select_related('collection').all()
#     serializer_class = ProductSerializer
    
#     def get_serializer_context(self):
#         return {'request':self.request}
        
# class ProductDetail(RetrieveUpdateDestroyAPIView):
#     queryset = Product.objects.all()
#     serializer_class = ProductSerializer

#     def delete(self,request, pk):
#         product = get_object_or_404(Product , pk=pk)
#         if product.orderitems.count() > 0:
#             return Response({'error':'product cannot be deleted as it is associated with OrderItem'},status=status.HTTP_405_METHOD_NOT_ALLOWED)
#         product.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)    
 

#Function based 
# @api_view(['GET' , 'POST'])
# def product_list(request):
#     if request.method == 'GET':
#         query_set = Product.objects.select_related('collection').all()
#         serializer = ProductSerializer(
#             query_set , many = True , context={'request':request})
#         return Response(serializer.data)
#     elif request.method == 'POST':
#         serializer = ProductSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         # print(serializer.validated_data)
#         return Response(serializer.data , status=status.HTTP_201_CREATED)
 
# @api_view(['GET' , 'PUT' , 'DELETE'])
# def product_detail(request,id):
#     #product = Product.objects.get(pk=id)
#     product = get_object_or_404(Product , pk=id)
#     if request.method == 'GET':
#         serializer = ProductSerializer(product)
#         return Response(serializer.data)
#     elif request.method == 'PUT':
#         serializer = ProductSerializer(product ,data = request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data)
#     elif request.method == 'DELETE':
#         if product.orderitems.count() > 0:
#             return Response({'error':'product cannot be deleted as it is associated with OrderItem'},status=status.HTTP_405_METHOD_NOT_ALLOWED)
#         product.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)

#Class Based View APIView
# class ProductList(APIView):
#     def get(self , request):
#         query_set = Product.objects.select_related('collection').all()
#         serializer = ProductSerializer(
#             query_set , many = True , context={'request':request})
#         return Response(serializer.data)
#     def post(self , request):
#         serializer = ProductSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data , status=status.HTTP_201_CREATED)

# class ProductDetail(APIView):
#     def get(self,request,id):
#         product = get_object_or_404(Product , pk=id)
#         serializer = ProductSerializer(product)
#         return Response(serializer.data)
#     def put(self , request,id):
#         product = get_object_or_404(Product , pk=id)
#         serializer = ProductSerializer(product ,data = request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data,id)
#     def delete(self,request):
#         product = get_object_or_404(Product , pk=id)
#         if product.orderitems.count() > 0:
#             return Response({'error':'product cannot be deleted as it is associated with OrderItem'},status=status.HTTP_405_METHOD_NOT_ALLOWED)
#         product.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)   


    
    


#Generic View
# class CollectionList(ListCreateAPIView):
#     queryset =query_set = Collection.objects.annotate(products_count = Count('products')).all()
#     serializer_class = CollectionSerializer

# class CollectionDetail(RetrieveUpdateDestroyAPIView):
#     queryset = Collection.objects.annotate(products_count=Count('products'))
#     serializer_class = CollectionSerializer
    
#     def delete(self, request , pk):
#         collection = get_object_or_404(Collection.objects.annotate(products_count=Count('products')) , pk=pk)
#         if collection.products.count() > 0:
#             return Response({'error':'collection cannot be deleted as associated with product' }, status=status.HTTP_405_METHOD_NOT_ALLOWED)
#         collection.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)
    
#Function Based   
# @api_view(['GET' ,'POST'])
# def collection_list(request):
#     if request.method == 'GET':
#         query_set = Collection.objects.annotate(products_count = Count('products')).all()
#         serializer = CollectionSerializer(query_set , many= True)
#         return Response(serializer.data)
#     elif request.method == 'POST':
#         serializer = CollectionSerializer(data = request.data) 
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data , status=status.HTTP_201_CREATED)
        
# @api_view(['GET' ,'PUT' , 'DELETE'])
# def collection_detail(request , pk):
#     collection = get_object_or_404( 
#         Collection.objects.annotate(
#             products_count=Count('products')) , pk=pk)
#     if request.method == 'GET':
#         serializer = CollectionSerializer(collection)
#         return Response(serializer.data)
#     elif request.method == 'PUT':
#         serializer = CollectionSerializer(collection , data = request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data)
#     elif request.method == 'DELETE':
#         if collection.products.count() > 0:
#             return Response({'error':'collection cannot be deleted as associated with product' }, status=status.HTTP_405_METHOD_NOT_ALLOWED)
#         collection.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)



    