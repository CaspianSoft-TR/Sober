
from rest_framework import serializers
from allauth.account.adapter import get_adapter
from allauth.account.utils import setup_user_email
from allauth.utils import (
    email_address_exists,
    get_username_max_length
)
from allauth.account import app_settings as allauth_settings
from rest_auth.registration.serializers import RegisterSerializer
from rest_auth.serializers import UserDetailsSerializer
from api.models import (
    UserInfo,
    Car,
    UserCar,
    Address,
    Booking,
    Driver
)


###########################################################

class UserSerializer(UserDetailsSerializer):
    phone = serializers.CharField(source="userinfo.phone")
    is_driver = serializers.BooleanField(source="userinfo.is_driver")
    is_customer = serializers.BooleanField(source="userinfo.is_customer")

    class Meta(UserDetailsSerializer.Meta):
        fields = UserDetailsSerializer.Meta.fields + ('phone','is_driver', 'is_customer')

    def update(self, instance, validated_data):
        print("DENEME")
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

    class Meta:
        model = UserInfo
        fields = ('user', 'phone')

    # Override CREATE method
    def create(self, validated_data):
        data = validated_data.copy()
        print("UserInfoSerializer >> CREATE called")
        return UserInfo.objects.create(**data)

    # Override UPDATE method
    def update(self, instance, validated_data):
        print("UserInfoSerializer >> UPDATE called")
        return instance


# CUSTOM REGISTER SERIALIZER
class RegisterSerializer(serializers.Serializer):
    username = serializers.CharField(
        max_length=get_username_max_length(),
        min_length=allauth_settings.USERNAME_MIN_LENGTH,
        required=allauth_settings.USERNAME_REQUIRED
    )
    email = serializers.EmailField(required=allauth_settings.EMAIL_REQUIRED)
    password1 = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)
    phone = serializers.CharField(source="userinfo.phone")
    is_driver = serializers.BooleanField(default=False)
    is_customer = serializers.BooleanField(default=True)

    def validate_username(self, username):
        username = get_adapter().clean_username(username)
        return username

    def validate_email(self, email):
        email = get_adapter().clean_email(email)
        if allauth_settings.UNIQUE_EMAIL:
            if email and email_address_exists(email):
                raise serializers.ValidationError(("A user is already registered with this e-mail address."))
        return email

    def validate_password1(self, password):
        return get_adapter().clean_password(password)

    def validate(self, data):
        if data['password1'] != data['password2']:
            raise serializers.ValidationError(("The two password fields didn't match."))
        return data

    def custom_signup(self, request, user):
        pass

    def get_cleaned_data(self):
        return {
            'username': self.validated_data.get('username', ''),
            'password1': self.validated_data.get('password1', ''),
            'email': self.validated_data.get('email', '')
        }

    def save(self, request):
        adapter = get_adapter()
        user = adapter.new_user(request)
        self.cleaned_data = self.get_cleaned_data()
        adapter.save_user(request, user, self)
        self.custom_signup(request, user)
        setup_user_email(request, user, [])
        user.save()

        newUserInfo = UserInfo()
        newUserInfo.phone = request.POST.get("phone", "")
        newUserInfo.is_customer = (request.POST.get("is_customer") == 'true' or request.POST.get("is_customer") == 'True')
        newUserInfo.is_driver = (request.POST.get("is_driver") == 'true' or request.POST.get("is_driver") == 'True')
        newUserInfo.user = user
        newUserInfo.save()

        #userInfoData = request.POST.copy()
        # print(">>>>>>>>>>>>><")
        #print(request.POST.get("phone", ""))
        # print(user.username)
        # print(">>>>>>>>>>>>><")

        # print(">>>>>>>>>>>>><")
        # print(userInfoData)
        # print(">>>>>>>>>>>>><")

        #userInfo = UserInfoSerializer(data=userInfoData)
        # is_valid() serializer data ile oluşması sonucu alınır
        # if userInfo.is_valid():
        # print(userInfo.validated_data)
        # print(user.username)
        # userInfo.save()

        # print(user)
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

# Driver National ID serializer


class DriverIDSerializer(serializers.ModelSerializer):
    class Meta:
        model = Driver
        fields = (

            'national_id',

        )

# Driver  DriverLicense serializer


class DriverLicenseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Driver
        fields = (

            'driver_license',

        )


class BookingAddressSerializer(serializers.ListSerializer):
    class Meta:
        model = Address
        fields = ('title', 'description', 'longitude', 'latitude')


class BookingSerializer(serializers.Serializer):

    id = serializers.SerializerMethodField()
    pickup_address_title = serializers.CharField(max_length=50)
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
        if data['payment_type'] < 0 and data['payment_type'] > 1:
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

        # find nearest userInfo
        #nearestDriverUserInfo = findNearestDriver(latitude=pickupAddress.latitude , longitude=pickupAddress.longitude , filterMaxDistance=10000)
        #newBook.driver = nearestDriverUserInfo.user
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


from rest_framework.renderers import JSONRenderer


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
