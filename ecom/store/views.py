from django.shortcuts import render
from django.http import JsonResponse
from .models import *
from .models import User
import json
# Create your views here.
def store(request):
    products=Product.objects.all()
    context={'products':products}
    return render(request,'store.html',context)

def  cart(request):
    if request.user.is_authenticated:
        customer=request.user.customer
        order,created=Order.objects.get_or_create(customer=customer,complete=False)
        items=order.orderitem_set.all()
    else:
        items=[]
    context={'items':items,'order':order}
    
    return render(request,'cart.html',context)

def checkout(request):
    if request.user.is_authenticated:
        customer=request.user.customer
        order,created=Order.objects.get_or_create(customer=customer,complete=False)
        items=order.orderitem_set.all()
    else:
        items=[]
    context={'items':items,'order':order}
    
    return render(request,'checkout.html',context)

def update_item(request):
    
    data =json.loads(request.body)
    productId=data['productId']
    action=data['action']
    print('action',action ,'productid',productId)
    customer=request.user.customer
    product=Product.objects.get(id=productId)
    order,created=Order.objects.get_or_create(customer=customer,complete=False)
    orderItem,created=OrderItem.objects.get_or_create(order=order,product=product)

    if action=='add':
        orderItem.quantity=orderItem.quantity+1
    elif action=='remove':
        orderItem.quantity=orderItem.quantity-1
    orderItem.save()

    if orderItem.quantity<=0:
        orderItem.delete()

    return JsonResponse('item was addded ',safe=False)