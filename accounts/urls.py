from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name='accounts'

urlpatterns = [
    path('', views.home, name='dashboard'),

    # Authentication
    path('register/', views.registerPage, name='register'),
    path('login/', views.loginPage, name='login'),
    path('logout/', views.logoutUser, name='logout'),
    
    # Password Reset 
                                 
    # 1- Submit password form                     // PasswordResetView.as_view() 
    # 2- Email sent success message               // PasswordResetDoneView.as_view()  
    # 3- Link to password reset form in email     // PasswordResetConfirmView.as_view() 
    # 4- password successfully changed message    // PasswordResetCompleteView.as_view()

    path('password_reset/', auth_views.PasswordResetView.as_view(template_name = 'accounts/password_reset_form.html') ,name='password_reset'),
    path('password_reset_sent/', auth_views.PasswordResetDoneView.as_view(template_name = 'accounts/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name = 'accounts/password_reset_confirm.html'), name='password_reset_confirm'),
    path('password_reset_complete/', auth_views.PasswordResetCompleteView.as_view(template_name = 'accounts/password_reset_complete.html'), name='password_reset_complete'),


    # Product
    path('products/', views.products, name='products'),
    path('update_product/<str:pk>/', views.updateProduct, name='update_product'),
    path('delete_product/<str:pk>/', views.deleteProduct, name='delete_product'),
    path('create_product/', views.createProduct, name='create_product'),

    # Customer 
    path('customer/<str:pk>/', views.customer, name='customer'),
    path('update_customer/<str:pk>/', views.updateCustomer, name='update_customer'),
    path('delete_customer/<str:pk>/', views.deleteCustomer, name='delete_customer'),
    path('create_customer/', views.createCustomer, name='create_customer'),
    
    # Order
    path('create_order/<str:pk>/', views.createOrder, name='create_order'),
    path('update_order/<str:pk>/', views.updateOrder, name='update_order'),
    path('delete_order/<str:pk>/', views.deleteOrder, name='delete_order'),

    # user
    path('profile/', views.userPage, name='profile'),
    path('profile/edit/', views.editProfile, name='edit_profile'),

]