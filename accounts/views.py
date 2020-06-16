from django.shortcuts import render
from .models import *
# Create your views here.

def home(request):

    context ={'home': home}
    return (request,"accounts/dashboard.html",context)

def products(request):

    context ={'home': home}
    return (request,"accounts/products.html",context)

def customer(request):

    context ={'home': home}
    return (request,"accounts/customers.html",context)        