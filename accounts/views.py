from django.shortcuts import render
from .models import *
# Create your views here.

def home(request):
    orders = Order.objects.all()
    customers = Customer.objects.all()
    total_orders = orders.count()
    total_cutomers = customers.count()
    delivered = orders.filter(status='Delivered').count()
    pending = orders.filter(status='Pending').count()

    context ={'orders': orders, 'customers':customers, 'total_orders':total_orders, 'total_cutomers':total_cutomers,
    'delivered':delivered, 'pending':pending}
    
    return render(request,"accounts/dashboard.html",context)

def products(request):
    products = Product.objects.all()

    context ={'products': products}

    return render(request,"accounts/products.html",context)

def customer(request,id):
    customer = Customer.objects.get(id=id)
    customer_orders = customer.order_set.all()
    customer_total_orders = customer_orders.count() 

    context ={'customer': customer, 'customer_orders':customer_orders, 'customer_total_orders':customer_total_orders}
    return render(request,"accounts/customers.html",context)        