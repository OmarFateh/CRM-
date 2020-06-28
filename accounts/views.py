from django.shortcuts import render, redirect
from django.forms import inlineformset_factory
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required


from django.contrib import messages
from django.core.paginator import Paginator
from .models import *
from .forms import OrderForm, CustomerForm, CreateUserForm

# Create your views here.

def registerPage(request):
    # if the user is logged in, this restricts him from visiting the register page and redirects him to the dashboard page 
    if request.user.is_authenticated:
        return redirect('accounts:dashboard')
    else:    
        if request.method == 'POST':
            form = CreateUserForm(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, f'Account was created for {user}.')
                return redirect('accounts:login')
        else:
            form = CreateUserForm()

        context = {'form': form}
        return render(request,'accounts/register.html',context)

def loginPage(request):
    if request.user.is_authenticated:
        return redirect('accounts:dashboard')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')           
            password = request.POST.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('accounts:dashboard')
            else:
                messages.info(request, 'Username or Password is incorrect')    
        context = {}
        return render(request,'accounts/login.html',context)

def logoutUser(request):
    logout(request)
    return redirect('accounts:login')    

@login_required(login_url='accounts:login')   #this restricts the user of visiting this page if he has not logged in yet and directs him to login page 
def home(request):
    # to show the orders in descending order according to creation date
    orders = Order.objects.all().order_by('-date_created')  #The negative sign indicates descending order.
    # Start Paginator
    paginator = Paginator(orders, 5)      # Show 2 jobs per page.
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    # End Paginator
    customers = Customer.objects.all()
    total_orders = orders.count()
    total_cutomers = customers.count()
    delivered = orders.filter(status='Delivered').count()
    pending = orders.filter(status='Pending').count()

    context ={'orders': page_obj, 'customers':customers, 'total_orders':total_orders, 'total_cutomers':total_cutomers,
    'delivered':delivered, 'pending':pending}
    
    return render(request,"accounts/dashboard.html",context)

@login_required(login_url='accounts:login')
def products(request):
    products = Product.objects.all()

    context ={'products': products}

    return render(request,"accounts/products.html",context)

@login_required(login_url='accounts:login')
def customer(request,pk):
    customer = Customer.objects.get(id=pk)
    customer_orders = customer.order_set.all().order_by('-date_created')
    customer_total_orders = customer_orders.count() 

    context ={'customer': customer, 'customer_orders':customer_orders, 'customer_total_orders':customer_total_orders}
    return render(request,"accounts/customers.html",context)        

@login_required(login_url='accounts:login')
def createOrder(request, pk):
    OrderFormSet = inlineformset_factory(Customer, Order , fields=('product','status'), extra=8)     # (parent model , child model , fields of child objects=(), extra=num of forms available)
    customer = Customer.objects.get(id=pk)
    if request.method == 'POST':
        formset = OrderFormSet(request.POST, instance=customer)
        if formset.is_valid():
            formset.save()
            return redirect('accounts:customer', pk=customer.id )
    else:
        formset = OrderFormSet(queryset=Order.objects.none(), instance=customer)      #queryset=Order.objects.none()=> to show zero item at the beginning     
        # form = OrderForm(initial={'customer':customer})        
    context = {'formset' : formset}        
    return render(request,'accounts/create_order.html', context)

@login_required(login_url='accounts:login')
def updateOrder(request, pk):
    order = Order.objects.get(id=pk)
    form = OrderForm(instance=order) 
    if request.method == 'POST':
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect('/')
    
    context = {'order': order , 'form':form}
    return render(request, 'accounts/update_order.html',context)    

@login_required(login_url='accounts:login')
def deleteOrder(request, pk):
    order = Order.objects.get(id=pk)
    if request.method == 'POST':
        order.delete()
        return redirect('/')

    context = {'order': order}
    return render(request, 'accounts/delete_order.html',context) 

@login_required(login_url='accounts:login')
def createCustomer(request):
    if request.method == "POST":
        form = CustomerForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')
    else:
        form = CustomerForm()

    context={'form':form}
    return render(request,'accounts/create_customer.html',context)

@login_required(login_url='accounts:login')    
def updateCustomer(request, pk):
    customer = Customer.objects.get(id=pk)
    form = CustomerForm(instance=customer) 
    if request.method == 'POST':    
        form = CustomerForm(request.POST, instance=customer)
        if form.is_valid():
            form.save()
            return redirect('accounts:customer', pk=customer.id )
    
    context = {"form": form}
    return render(request,'accounts/update_customer.html',context)    