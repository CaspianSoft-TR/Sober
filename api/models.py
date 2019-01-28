from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser
from decimal import Decimal

class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(default=None, blank=True, null=True)
    class Meta:
        abstract=True

class UserInfo(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=50)
    def __str__(self):
        return self.phone


class Car(BaseModel):
    brand = models.CharField(max_length=50)
    model = models.CharField(max_length=50)
    modelyear = models.IntegerField()
    added_by = models.ForeignKey(User, on_delete=models.CASCADE)
    def __str__(self):
        return self.car_brand


class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    contact_info = models.CharField(max_length=50)
    def __str__(self):
        return self.contact_info


class UserCar(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    number_plate = models.CharField(max_length=20)
    color = models.CharField(max_length=100, default="")
    gear_type = models.IntegerField(choices=((0, 'UNKNOWN'), (1, 'AUTO'), (2, 'MANUAL')), default=2) 
    def __str__(self):
        return self.number_plate


class Category (models.Model):
    pickup_location = models.CharField(max_length=20)
    arrival_destination = models.CharField(max_length=20)
    def __str__(self):
        return self.pickup_location


class Driver(models.Model):
    #driver_id = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    #vehicle = models.ForeignKey(Car, on_delete=models.CASCADE)
    phone = models.CharField(max_length=50)
    def __str__(self):
        return self.phone


class DriverLocation (models.Model):
    driver_id = models.ForeignKey(Driver, on_delete=models.CASCADE)
    longitude = models.CharField(max_length=10)
    latitude = models.CharField(max_length=10)
    location_name = models.CharField(max_length=20)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    def __str__(self):
        return self.location_name


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
