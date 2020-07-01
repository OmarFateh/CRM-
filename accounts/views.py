from django.shortcuts import render, redirect
from django.forms import inlineformset_factory
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group

from django.contrib import messages
from django.core.paginator import Paginator
from .models import *
from .forms import OrderForm, CustomerForm, CreateUserForm, ProductForm
from .decorators import unauthenticated_user, allowed_users
from .filters import OrderFilter


# ------- Start Authentication ---------
@unauthenticated_user
def registerPage(request):
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account was created for {username}.')
            return redirect('accounts:login')
    else:
        form = CreateUserForm()

    context = {'form': form}
    return render(request,'accounts/register.html',context)

@unauthenticated_user
def loginPage(request):
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

# ----- End Authentication -------

# -----Start Admin ---------

# Start Home
@login_required(login_url='accounts:login')   #this restricts the user of visiting this page if he has not logged in yet and directs him to login page 
@allowed_users(allowed_roles=['admin'])
def home(request):
    # to show the orders in descending order according to creation date
    orders = Order.objects.all().order_by('-date_created')  #The negative sign indicates descending order.
    # Start Paginator
    paginator = Paginator(orders, 5)      # Show 5 orders per page.
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

# End Home
# Start Products
@login_required(login_url='accounts:login')
@allowed_users(allowed_roles=['admin'])
def products(request):
    products = Product.objects.all()
    # Start Paginator
    paginator = Paginator(products, 3)      # Show 3 orders per page.
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    # End Paginator
    
    context ={'products': page_obj}
    return render(request,"accounts/products.html",context)

@login_required(login_url='accounts:login')
@allowed_users(allowed_roles=['admin'])
def createProduct(request):
    if request.method == "POST":
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('accounts:products')
    else:
        form = ProductForm()

    context = {'form':form}
    return render(request,"accounts/create_product.html",context)

@login_required(login_url='accounts:login')
@allowed_users(allowed_roles=['admin'])
def updateProduct(request,pk):
    product = Product.objects.get(id=pk)
    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            return redirect('accounts:products')
    else:
        form = ProductForm(instance=product) 
    context = {'form':form}
    return render(request,"accounts/update_product.html",context)

@login_required(login_url='accounts:login')
@allowed_users(allowed_roles=['admin'])
def deleteProduct(request,pk):
    product = Product.objects.get(id=pk)
    if request.method == 'POST':
        product.delete()
        return redirect('accounts:products')
    
    context = {'product':product}
    return render(request,"accounts/delete_product.html",context)

# End Products
# Start Order
@login_required(login_url='accounts:login')
@allowed_users(allowed_roles=['admin'])
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
    context = {'formset' : formset, 'customer':customer}        
    return render(request,'accounts/create_order.html', context)

@login_required(login_url='accounts:login')
@allowed_users(allowed_roles=['admin'])
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
@allowed_users(allowed_roles=['admin'])
def deleteOrder(request, pk):
    order = Order.objects.get(id=pk)
    if request.method == 'POST':
        order.delete()
        return redirect('/')

    context = {'order': order}
    return render(request, 'accounts/delete_order.html',context) 

# End Order
# Start Customer
@login_required(login_url='accounts:login')
@allowed_users(allowed_roles=['admin'])
def customer(request,pk):
    customer = Customer.objects.get(id=pk)
    # Start orders filter
    customer_orders = customer.order_set.all().order_by('-date_created')
    orders_filter = OrderFilter(request.GET, queryset=customer_orders)
    customer_orders = orders_filter.qs
    # End orders filter 
    customer_total_orders = customer_orders.count() 

    context ={'customer': customer, 'customer_orders':customer_orders, 'customer_total_orders':customer_total_orders, 
              'orders_filter':orders_filter}
    return render(request,"accounts/customers.html",context)      

@login_required(login_url='accounts:login')
@allowed_users(allowed_roles=['admin'])
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
@allowed_users(allowed_roles=['admin']) 
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

@login_required(login_url='accounts:login')
@allowed_users(allowed_roles=['admin'])
def deleteCustomer(request,pk):
    customer = Customer.objects.get(id=pk)
    if request.method == 'POST':
        customer.delete()
        return redirect('accounts:dashboard')
    
    context = {'customer':customer}
    return render(request,"accounts/delete_customer.html",context)    

# End Customer    

# -----End Admin --------- 

# -----Start User ---------

@login_required(login_url='accounts:login')
@allowed_users(allowed_roles=['customer'])
def userPage(request):
    orders = request.user.customer.order_set.all().order_by('-date_created')
    total_orders = orders.count()
    delivered = orders.filter(status='Delivered').count()
    pending = orders.filter(status='Pending').count()
    # Start Paginator
    paginator = Paginator(orders, 2)      # Show 2 orders per page.
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    # End Paginator
    context = {'orders': page_obj, 'total_orders':total_orders,
    'delivered':delivered, 'pending':pending}
    return render(request,"accounts/profile.html",context)

@login_required(login_url='accounts:login')
@allowed_users(allowed_roles=['customer'])
def editProfile(request):
    customer = request.user.customer
    if request.method == 'POST':
        form = CustomerForm(request.POST, request.FILES, instance=customer)
        if form.is_valid():
            form.save()
            print("done")
            # return redirect('accounts:profile')
    else:
        form = CustomerForm(instance=customer)
    context = {'form':form}
    return render(request,'accounts/edit_profile.html',context)

# -----End User ---------