from django.shortcuts import render
from django.http import HttpResponse

def calculate():
    x = 1
    y =2
    return x

# Create your views here.
def say_hello(request):
    x=calculate()
    
    #return HttpResponse('Hello world') 
    return render(request , 'hello.html')