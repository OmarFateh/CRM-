from django.urls import path
from . import views

app_name='accounts'

urlpatterns = [
    path('', views.home, name='dashboard'),

    path('register/', views.registerPage, name='register'),
    path('login/', views.loginPage, name='login'),
    path('logout/', views.logoutUser, name='logout'),

    path('products/', views.products, name='products'),

    path('customer/<str:pk>/', views.customer, name='customer'),
    path('update_customer/<str:pk>/', views.updateCustomer, name='update_customer'),
    path('create_customer/', views.createCustomer, name='create_customer'),
    
    path('create_order/<str:pk>/', views.createOrder, name='create_order'),
    path('update_order/<str:pk>/', views.updateOrder, name='update_order'),
    path('delete_order/<str:pk>/', views.deleteOrder, name='delete_order'),

]