from django.contrib.auth import password_validation
from django.contrib.auth.models import User
from django.db.models import Avg
from rest_auth.serializers import UserDetailsSerializer
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from api.models import (
    UserInfo,
    Car,
    UserCar,
    Address,
    Booking,
    Document)


###########################################################

class UserSerializer(UserDetailsSerializer):
    password = serializers.CharField()
    phone = serializers.CharField(source="userinfo.phone")
    is_driver = serializers.BooleanField(source="userinfo.is_driver")
    is_customer = serializers.BooleanField(source="userinfo.is_customer")

    class Meta(UserDetailsSerializer.Meta):
        fields = UserDetailsSerializer.Meta.fields + ('phone', 'is_driver', 'is_customer', 'password')

    def validate_password(self, value):
        password_validation.validate_password(value, self.instance)
        return value

    def create(self, validated_data):
        password = validated_data.pop('password')
        profile_data = validated_data.pop('userinfo')
        user = User(**validated_data)
        user.set_password(password)
        user.save()

        UserInfo.objects.create(user=user, **profile_data)

        return user

    def update(self, instance, validated_data):
        profile_data = validated_data.pop('userinfo', {})
        phone = profile_data.get('phone')

        instance = super(UserSerializer, self).update(instance, validated_data)

        # get and update user profile
        profile = instance.userinfo
        if profile_data and phone:
            profile.phone = phone
            profile.save()
        return instance


class UserInfoSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    rating = serializers.SerializerMethodField()

    def get_rating(self, obj):
        driver_rate = Booking.objects.all().aggregate(Avg('driver_rate'))
        return driver_rate['driver_rate__avg']

    class Meta:
        model = UserInfo
        fields = ('phone', 'latitude', 'longitude', 'rating', 'user')

    # Override CREATE method
    def create(self, validated_data):
        data = validated_data.copy()
        print("UserInfoSerializer >> CREATE called")
        return UserInfo.objects.create(**data)

    # Override UPDATE method
    def update(self, instance, validated_data):
        print("UserInfoSerializer >> UPDATE called")
        return instance


class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = ('national_id', 'driver_license')


# Driver National ID serializer
class DriverIDSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = ('national_id',)

    def create(self, validated_data):
        user = validated_data.pop('user')
        driver = Document.objects.create(user=user, **validated_data)
        return driver

    def update(self, instance, validated_data):
        user = validated_data.pop('user')
        national_id = validated_data.pop('national_id')
        instance.user = user
        # first delete old image with source from server
        instance.national_id.delete(False)
        instance.national_id = national_id
        instance.save()

        return instance


# Driver  DriverLicense serializer
class DriverLicenseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = ('driver_license',)

    def create(self, validated_data):
        user = validated_data.pop('user')
        driver = Document.objects.create(user=user, **validated_data)
        return driver

    def update(self, instance, validated_data):
        user = validated_data.pop('user')
        driver_license = validated_data.pop('driver_license')
        instance.user = user
        # first delete old image with source from server
        instance.driver_license.delete(False)
        instance.driver_license = driver_license
        instance.save()

        return instance


#  CUSTOM REGISTER SERIALIZER
class RegisterSerializer(UserSerializer):
    document = DocumentSerializer(required=False)

    email = serializers.EmailField(
        max_length=100,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )

    national_id = serializers.ImageField(source='document.national_id', required=False, default=None)
    driver_license = serializers.ImageField(source='document.driver_license', required=False, default=None)

    class Meta(UserSerializer.Meta):
        fields = UserSerializer.Meta.fields + ('email', 'national_id', 'driver_license', 'document')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        password = validated_data.pop('password')
        profile_data = validated_data.pop('userinfo')
        document = validated_data.pop('document')

        user = User(**validated_data)
        user.set_password(password)
        user.save()

        UserInfo.objects.create(user=user, **profile_data)
        Document.objects.create(user=user, **document)
        return user


# Verify Email
class VerifyEmailSerializer(serializers.Serializer):
    key = serializers.CharField()


###############################################################################


class CarDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Car
        fields = ('brand', 'model', 'modelyear', 'added_by')


class CarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Car
        fields = ('brand', 'model', 'modelyear')


class UserCarSerializer(serializers.ModelSerializer):
    car_id = serializers.IntegerField()

    class Meta:
        model = UserCar
        fields = ('number_plate', 'color', 'gear_type', 'car_id')


class UserAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ('title', 'description', 'longitude', 'latitude')


class BookingAddressSerializer(serializers.ListSerializer):
    class Meta:
        model = Address
        fields = ('title', 'description', 'longitude', 'latitude')


class CreateBookingSerializer(serializers.Serializer):
    id = serializers.SerializerMethodField()
    pickup_address_title = serializers.CharField(max_length=50, required=True)
    pickup_address_description = serializers.CharField(max_length=255)
    pickup_address_longitude = serializers.CharField(max_length=30, default=0)
    pickup_address_latitude = serializers.CharField(max_length=30, default=0)
    arrival_address_title = serializers.CharField(max_length=50)
    arrival_address_description = serializers.CharField(max_length=50)
    arrival_address_longitude = serializers.CharField(max_length=30, default=0)
    arrival_address_latitude = serializers.CharField(max_length=30, default=0)
    payment_type = serializers.IntegerField(default=0)
    price = serializers.IntegerField(default=0)
    distance = serializers.IntegerField(default=0)

    def get_id(self, obj):
        return self.validated_data['book_id']

    def validate(self, data):
        payment_type = data['payment_type']
        if payment_type > 1 or payment_type < 0:
            raise serializers.ValidationError(("Payment type should be 0 for cash and 1 for credit card"))
        return data

    def save(self, request):
        newBook = Booking()
        newBook.customer = request.user
        newBook.payment_type = request.POST.get("payment_type")
        newBook.price = request.POST.get("price")
        newBook.total_distance = request.POST.get("total_distance")
        newBook.save()
        self.validated_data['book_id'] = newBook.id

        pickupAddress = Address()
        pickupAddress.title = request.POST.get("pickup_address_title")
        pickupAddress.description = request.POST.get("pickup_address_description")
        pickupAddress.longitude = request.POST.get("pickup_address_longitude")
        pickupAddress.latitude = request.POST.get("pickup_address_latitude")
        pickupAddress.is_pickup_loc = True
        pickupAddress.booking = newBook
        pickupAddress.save()

        arrivalAddress = Address()
        arrivalAddress.title = request.POST.get("arrival_address_title")
        arrivalAddress.description = request.POST.get("arrival_address_description")
        arrivalAddress.longitude = request.POST.get("arrival_address_longitude")
        arrivalAddress.latitude = request.POST.get("arrival_address_latitude")
        arrivalAddress.is_arrival_loc = True
        arrivalAddress.booking = newBook
        arrivalAddress.save()

        #  find nearest userInfo
        # nearestDriverUserInfo = findNearestDriver(latitude=pickupAddress.latitude , longitude=pickupAddress.longitude , filterMaxDistance=10000)
        # newBook.driver = nearestDriverUserInfo.user
        return newBook


########################################
# TEST SERIALIZER
########################################
from datetime import datetime


class TestClass(object):
    def __init__(self, email, content, created=None):
        self.email = email
        self.content = content
        self.created = created or datetime.now()


class TESTSerializer(serializers.Serializer):
    email = serializers.EmailField()
    content = serializers.CharField(max_length=200)
    created = serializers.DateTimeField()

    def create(self, validated_data):
        print(">>> >>> TESTSerializer update CALLED ")
        print(type(validated_data))

        testClass = TestClass(email='ksk@example.com', content='TEST Content')
        # return JSONRenderer().render(validated_data)
        return testClass

    def update(self, instance, validated_data):
        print(">>> >>> TESTSerializer update CALLED ")
        instance.email = validated_data.get('email', instance.email)
        instance.content = validated_data.get('content', instance.content)
        instance.created = validated_data.get('created', instance.created)
        return instance


class BookSerializer(serializers.ModelSerializer):
    driver = UserDetailsSerializer()
    customer = UserDetailsSerializer()
    pickUp_address = serializers.SerializerMethodField()
    dropOff_address = serializers.SerializerMethodField()

    def get_pickUp_address(self, obj):
        address = Address.objects.filter(booking_id=obj.id, is_pickup_loc=1).first()
        serializer = UserAddressSerializer(address)
        return serializer.data

    def get_dropOff_address(self, obj):
        address = Address.objects.filter(booking_id=obj.id, is_pickup_loc=0).first()
        serializer = UserAddressSerializer(address)
        return serializer.data

    class Meta:
        fields = ('id', 'status', 'total_distance', 'price', 'driver', 'customer', 'pickUp_address', 'dropOff_address', 'room_id')
        model = Booking
