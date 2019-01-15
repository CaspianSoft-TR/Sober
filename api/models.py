from django.db import models

# Create your models here.


class MyTest(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


class MyStore(models.Model):
    #mytest = models.ForeignKey(MyTest)
    storeName = models.CharField(max_length=255, unique=True)
    storeId = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.storeName


###################################
from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser
from decimal import Decimal
from payments import PurchasedItem
from payments.models import BasePayment


class CustomUser(AbstractUser):
    # name = models.CharField(blank=True, max_length=255)
    user_type = models.IntegerField(choices=((0, 'CUSTOMER'), (1, 'DRIVER')), default=0)

    def __str__(self):
        return self.email


class Driver(models.Model):
    driver_id = models.AutoField(primary_key=True)

    name = models.OneToOneField(User, on_delete=models.CASCADE)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=200)
    vehicle = models.ForeignKey(Car, on_delete=models.CASCADE)
    pickup_location = models.ForeignKey(Location, on_delete=models.CASCADE)
    phone = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Customer(models.Model):
    customer_id = models.AutoField(primary_key=True)

    name = models.OneToOneField(User, related_name='rider_profile', on_delete=models.CASCADE)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=200)
    current_location = models.ForeignKey(Location, related_name='current_location', on_delete=models.CASCADE, null=True)
    pickup_location = models.ForeignKey(Location, related_name='rider_pickup', on_delete=models.CASCADE)
    contact_info = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Car(models.Model):

    car_brand = models.CharField(max_length=50)
    number_plate = models.CharField(max_length=20)

    def __str__(self):
        return self.car_brand


class DriverLocation (models.Model):
    driver_id = models.ForeignKey(Driver, on_delete=models.CASCADE)
    longitude = models.CharField(max_length=10)
    latitude = models.CharField(max_length=10)
    location_name = models.CharField(max_length=20)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return self.location_name


class Category (models.Model):

    pickup_location = models.CharField(max_length=20)
    arrival_destination = models.CharField(max_length=20)

    def __str__(self):
        return self.pickup_location


class Transaction (models.Model):

    order_id = models.AutoField(primary_key=True)
    driver_id = models.ForeignKey(Driver, on_delete=models.CASCADE)
    customer_id = models.ForeignKey(Customer, on_delete=models.CASCADE)

    def __str__(self):
        return self.order_id


class Review (models.Model):

    review_id = models.AutoField(primary_key=True)
    driver_id = models.ForeignKey(Driver, on_delete=models.CASCADE)
    customer_id = models.ForeignKey(Customer, on_delete=models.CASCADE)
    comment = models.CharField(max_length=200)

    def __str__(self):
        return self.order_id


class Payment(BasePayment):

    def __str__(self):
        return self.payment_id


class DriverHistory(models.Model):

    driver_id = models.ForeignKey(Driver, on_delete=models.CASCADE)
    customer_id = models.ForeignKey(Customer, on_delete=models.CASCADE)
    pickup_location = models.CharField(Category, max_length=20)
    arrival_destination = models.CharField(Category, max_length=20)
    booked_time = models.DateTimeField(auto_now_add=True)


class TravelHistory(models.Model):
    customer_id = models.ForeignKey(Customer, on_delete=models.CASCADE)
    driver_id = models.ForeignKey(Driver, on_delete=models.CASCADE)
    pickup_location = models.CharField(Category, max_length=20)
    arrival_destination = models.CharField(Category, max_length=20)
    booked_time = models.DateTimeField(auto_now_add=True)


class Booking(models.Model):
    customer_id = models.ForeignKey(Customer, on_delete=models.CASCADE)
    driver_id = models.ForeignKey(Driver, on_delete=models.CASCADE)
    # customer = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    # driver = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, related_name='booking_driver')
    status = models.IntegerField(choices=((0, 'NEW'), (1, 'ACCEPTED'), (2, 'REJECTED')), default=0)

    def __str__(self):
        return 'Booking from #{}'.format(self.customer.username)
