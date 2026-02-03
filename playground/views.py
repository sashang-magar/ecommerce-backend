from django.shortcuts import render
from django.http import HttpResponse
from store.models import Product
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q , F

from django.contrib.contenttypes.models import ContentType
from store.models import Product 
from tags.models import TaggedItem


# Create your views here.
def say_hello(request):

 #just to call custom manager from tags app model
    # query_set = TaggedItem.objects.get_tags_for(Product, 1)
    # return render(request , 'hello.html', {'tags': list(query_set)} )

    return render(request , 'hello.html')

#we can use first() , exists() instead of try catch 
    # try:
    #     product= Product.objects.get(id=1111)
    # except ObjectDoesNotExist:
    #     pass    
    #return HttpResponse('Hello world') 

    # exists = Product.objects.filter(id=66).exists() #return boolean,no queryset
    # if exists:
    #     return "Username exists"
    # else:
    #     print("Not found")
    # product = Product.objects.filter(inventory=F('unit_price'))    
    # return render(request , 'hello.html' , {'product': list(product)})

    