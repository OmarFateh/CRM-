from django.db import models
from django.contrib.auth.models import User
# Create your models here.

def profile_pic_upload(instance,filename):
    imagename, extension = filename.split(".")
    path = f"profile_pics/{instance.id}.{extension}"
    return path

class Customer(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE) # to have one to one relationship with User model
    name = models.CharField(max_length=20, null=True)
    phone = models.CharField(max_length=20, null=True)
    email = models.CharField(max_length=20, null=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    picture = models.ImageField(upload_to=profile_pic_upload, default='profile_pics/2.png', null=True, blank=True)

    def __str__(self):
        return str(self.name)


class Tag(models.Model):  
    name = models.CharField(max_length=20, null=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    CATEGORY=(
        ("In Door", 'In Door'),
        ("Out Door", "Out Door"),
    )

    name = models.CharField(max_length=20, null=True)
    price = models.FloatField(max_length=20, null=True)
    description = models.TextField(max_length=200, null=True , blank=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    category = models.CharField(max_length=20, null=True, choices=CATEGORY)
    tags = models.ManyToManyField(Tag)

    def __str__(self):
        return self.name


class Order(models.Model):
    STATUS= (
        ("Out for Delivery", 'Out for Delivery'),
        ("Delivered", 'Delivered'),
        ("Pending", "Pending"),
    )

    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    status = models.CharField(max_length=30, null=True, choices=STATUS)
    note = models.CharField(max_length=50, null=True)
    
    def __str__(self):
        return self.product.name
