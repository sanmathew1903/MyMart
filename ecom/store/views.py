from django.shortcuts import render
from django.http import JsonResponse
from .models import *
from .models import User
import json
import datetime

from .utils import *
# Create your views here.
def store(request):

    data=cartData(request)
    cartItems=data['cartItems']

    products=Product.objects.all()
    context={'products':products,'cartItems':cartItems}
    
    return render(request,'store.html',context)

def  cart(request):
    
    data=cartData(request)
    cartItems=data['cartItems']
    order=data['order']
    items=data['items']

    context={'items':items,'order':order,'cartItems':cartItems}
    
    return render(request,'cart.html',context)

def checkout(request):
    data=cartData(request)
    cartItems=data['cartItems']
    order=data['order']
    items=data['items']

    context={'items':items,'order':order,'cartItems':cartItems}
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
        

def processOrder(request):
    
    transaction_id=datetime.datetime.now().timestamp()
    data=json.loads(request.body)

    if request.user.is_authenticated:
        print("authenticated")
        customer=request.user.customer
        order,created=Order.objects.get_or_create(customer=customer,complete=False)
        total=float(data['form']['total'])
        order.transaction_id=transaction_id

        if total==order.get_cart_total:
            order.complete=True
        order.save()        

        if order.shipping==True:
            ShippingAddress.objects.create(
                customer=customer,
                order=order,
                city=data['shipping']['city'],
                address=data['shipping']['address'],
                state=data['shipping']['state'],
                zipcode=data['shipping']['zipcode'],
            )
    else:
        print('user not logged')

    return JsonResponse('Payment complete' ,safe=False)