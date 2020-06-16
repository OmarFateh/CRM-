from django.db import models

# Create your models here.

class Customer(models.Model):
    name = models.CharField(max_length=20, null=True)
    phone = models.IntegerField(null=True)
    email = models.CharField(max_length=20, null=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.name


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
    
