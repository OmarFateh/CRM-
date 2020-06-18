from django.urls import path
from . import views

app_name='accounts'

urlpatterns = [
    path('', views.home, name='dashboard'),
    path('products/', views.products, name='products'),
    path('customer/<int:id>', views.customer, name='customer'),
]