from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser
from decimal import Decimal


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(default=None, blank=True, null=True)

    class Meta:
        abstract = True


class UserInfo(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_driver = models.BooleanField(default=False)
    is_customer = models.BooleanField(default=True)
    phone = models.CharField(max_length=50)
    longitude = models.CharField(max_length=10, default=0)
    latitude = models.CharField(max_length=10, default=0)
    firebase_token = models.CharField(max_length=255, default="")
    def __str__(self):
        return self.phone


class Driver(models.Model):
    #driver_id = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    #vehicle = models.ForeignKey(Car, on_delete=models.CASCADE)
    phone = models.CharField(max_length=50)
    national_id = models.ImageField(upload_to='sober/static/national_id',blank=True)
    driver_license = models.ImageField(upload_to='sober/static/driving_license',blank=True)

    def __str__(self):
        return self.phone


class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    contact_info = models.CharField(max_length=50)

    def __str__(self):
        return self.contact_info


class Car(BaseModel):
    brand = models.CharField(max_length=50)
    model = models.CharField(max_length=50)
    modelyear = models.IntegerField()
    added_by = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.car_brand


class UserCar(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    car = models.ForeignKey(Car, on_delete=models.CASCADE, default=1)
    number_plate = models.CharField(max_length=20)
    color = models.CharField(max_length=100, default="")
    gear_type = models.IntegerField(choices=((0, 'UNKNOWN'), (1, 'AUTO'), (2, 'MANUAL')), default=2)

    def __str__(self):
        return self.number_plate


class Booking(BaseModel):
    customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='customer_id')
    driver = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='driver_id')
    status = models.IntegerField(choices=((0, 'NEW'), (1, 'ACCEPTED'), (2, 'REJECTED'), (100, 'CANCEL')), default=0)
    payment_type = models.IntegerField(choices=((0, 'CASH'), (1, 'CREDIT CARD')), default=0)
    driver_rate = models.IntegerField(null=True, validators=[MaxValueValidator(5), MinValueValidator(0)])

    def __str__(self):
        return 'Booking from #{}'.format(self.customer.username)


class Address(models.Model):
    booking = models.ForeignKey(Booking, null=True, on_delete=models.CASCADE, related_name='booking_id')
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE, related_name='user_id')
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=50)
    longitude = models.CharField(max_length=10, default=0)
    latitude = models.CharField(max_length=10, default=0)
    is_pickup_loc = models.BooleanField(default=False)
    is_arrival_loc = models.BooleanField(default=False)

    def __str__(self):
        return 'address'


###
class DriverLocation (models.Model):
    driver_id = models.ForeignKey(Driver, on_delete=models.CASCADE)
    longitude = models.CharField(max_length=10)
    latitude = models.CharField(max_length=10)
    location_name = models.CharField(max_length=20)
    #category = models.ForeignKey(Category, on_delete=models.CASCADE)

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
    #pickup_location = models.CharField(Category, max_length=20)
    #arrival_destination = models.CharField(Category, max_length=20)
    booked_time = models.DateTimeField(auto_now_add=True)


class TravelHistory(models.Model):
    customer_id = models.ForeignKey(Customer, on_delete=models.CASCADE)
    driver_id = models.ForeignKey(Driver, on_delete=models.CASCADE)
    #pickup_location = models.CharField(Category, max_length=20)
    #arrival_destination = models.CharField(Category, max_length=20)
    booked_time = models.DateTimeField(auto_now_add=True)
