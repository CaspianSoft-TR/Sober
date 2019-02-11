
from django.contrib.auth.models import User, Group
from django.contrib.auth.hashers import make_password
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAdminUser
from rest_framework.decorators import api_view
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.generics import (
    ListAPIView,
    UpdateAPIView,
    CreateAPIView,
    DestroyAPIView,
)
from rest_framework.views import APIView
from rest_framework import viewsets, status
from rest_auth.registration.views import RegisterView
from . import models
from . import serializers
from api.serializers import *



import googlemaps
gmaps = googlemaps.Client(key='AIzaSyA2b8Zh0rzAJQjwDn0_CZ_tHdPXm6G2Sjs')

def findNearestDriver(latitude , longitude , filterMaxDistance):
    # -1- GET ALL PROPER DRIVERS & LOCATION
    # -2- CALL GOOGLEMAPS API TO FIND DISTANCE
    # -3- IF DISTANCE <= 5000 
    userProfileList = UserInfo.objects.all()
    driverList = userProfileList.filter(is_driver=True)

    driverObjectList = []
    destinations = ''
    for driver in driverList:
        if not(driver.longitude=='0' and driver.latitude=='0'):

            if destinations == '':
                destinations = driver.latitude + ',' + driver.longitude
            else:
                destinations = destinations + '|' + driver.latitude + ',' + driver.longitude

            driverObjectList.append(driver)


    minDistanceIndex = -1
    minDistance = -1
    distanceResult = gmaps.distance_matrix(origins= latitude+','+longitude,destinations=destinations)
    for row in distanceResult['rows']:
        elementIndex = 0
        for element in row['elements']:
            distance = element['distance']
            if filterMaxDistance > distance['value']:
                if minDistance==-1 or distance['value'] < minDistance:
                    minDistance = distance['value']
                    minDistanceIndex = elementIndex

            elif distance['value'] >= minDistance:
                print("ERROR >> Distance filter error")
                        
            elementIndex=elementIndex+1
    return driverObjectList[minDistanceIndex]


def getDriverPoint():
    return 3


########################################
# USER SERVICES
########################################

class RegisterView(RegisterView):
    def get_serializer_class(self):
        return RegisterSerializer


class UserLocationUpdateAPIView(APIView):
    def get_queryset(self):
        queryset = UserInfo.objects.filter(user=self.request.user.id)
        return queryset

    def put(self, request, format=None):
        print(">>> >>> UserLocationUpdateAPIView put called")
        userInfo = self.get_queryset()
        print(type(userInfo))
        result = {}
        
        if userInfo.count() == 0:
            result["resultCode"] = 200
            result["resultText"] = "SUCCESS_EMPTY"
            result["content"] = "User Profile Not Found Error"
        elif userInfo.count() > 1:
            result["resultCode"] = 200
            result["resultText"] = "FAILURE"
            result["content"] = "Multiple User Profile Error"
        else:
            userProfile = userInfo.first()
            userProfile.longitude = self.request.POST.get('longitude')
            userProfile.latitude = self.request.POST.get('latitude')
            userProfile.save()
            result["resultCode"] = 100
            result["resultText"] = "SUCCESS"
            result["content"] = "User Location Updated"
        
        return JsonResponse(result)


########################################
# CAR SERVICES
########################################
class CarListAPIView(ListAPIView):
    queryset = Car.objects.all()
    serializer_class = CarSerializer

    def list(self, request):
        queryset = self.get_queryset()
        serializer = CarSerializer(queryset, many=True)
        result = {}
        result["resultCode"] = 100
        result["resultText"] = "SUCCESS"
        result["content"] = serializer.data
        return JsonResponse(result)


class CarCreateAPIView(CreateAPIView):
    queryset = Car.objects.all()
    serializer_class = CarSerializer
    permission_classes = (IsAdminUser,)
    authentication_classes = (TokenAuthentication,)

    def perform_create(self, serializer):
        serializer.save(added_by=self.request.user)
        # aşağıdaki degerleri return etmesi gerekir
        result = {}
        result["resultCode"] = 100
        result["resultText"] = "SUCCESS"
        result["content"] = serializer.data
        return JsonResponse(result)


########################################
#  USERCAR
########################################
class UserCarCreateAPIView(CreateAPIView):
    queryset = UserCar.objects.all()
    serializer_class = UserCarSerializer
    #permission_classes = (IsAdminUser,)
    #authentication_classes = (TokenAuthentication,)

    def perform_create(self, serializer):
        #carId = Car.objects.get(id=serializer.validated_data['car_idx'])
        # print(serializer.validated_data['car_idx'])

        serializer.save(user=self.request.user)
        print(">>> >>> UserCarCreateAPIView CALLED ")
        result = {}
        result["resultCode"] = 100
        result["resultText"] = "SUCCESS"
        result["content"] = serializer.data
        return JsonResponse(result)


class UserCarListAllAPIView(ListAPIView):
    queryset = UserCar.objects.all()
    serializer_class = UserCarSerializer
    #permission_classes = (IsAdminUser,)
    #authentication_classes = (TokenAuthentication,)

    def list(self, request):
        queryset = self.get_queryset()
        serializer = UserCarSerializer(queryset, many=True)
        result = {}
        result["resultCode"] = 100
        result["resultText"] = "SUCCESS"
        result["content"] = serializer.data
        return JsonResponse(result)


class UserCarDeleteAPIView(DestroyAPIView):
    serializer_class = UserCarSerializer
    #permission_classes = (IsAdminUser,)
    #authentication_classes = (TokenAuthentication,)

    def get_queryset(self):
        queryset = UserCar.objects.filter(user_id=self.request.user.id, id=self.kwargs['pk'])
        return queryset


########################################
#  USER ADDRESS
########################################
class UserAddressCreateAPIView(CreateAPIView):
    queryset = Address.objects.all()
    serializer_class = UserAddressSerializer
    #permission_classes = (IsAdminUser,)
    #authentication_classes = (TokenAuthentication,)

    def perform_create(self, serializer):
        print(">>> >>> UserAddressCreateAPIView CALLED ")
        serializer.save(user=self.request.user)
        result = {}
        result["resultCode"] = 100
        result["resultText"] = "SUCCESS"
        result["content"] = serializer.data
        return JsonResponse(result)


class UserAddressListAPIView(ListAPIView):
    queryset = Address.objects.all()
    serializer_class = UserAddressSerializer
    #permission_classes = (IsAdminUser,)
    #authentication_classes = (TokenAuthentication,)

    def list(self, request):
        queryset = self.get_queryset()
        queryset = queryset.filter(user_id=self.request.user.id)
        serializer = UserAddressSerializer(queryset, many=True)
        result = {}
        result["resultCode"] = 100
        result["resultText"] = "SUCCESS"
        result["content"] = serializer.data
        return JsonResponse(result)


class UserAddressListAllAPIView(ListAPIView):
    queryset = Address.objects.all()
    serializer_class = UserAddressSerializer
    permission_classes = (IsAdminUser,)
    #authentication_classes = (TokenAuthentication,)

    def list(self, request):
        queryset = self.get_queryset()
        serializer = UserAddressSerializer(queryset, many=True)
        result = {}
        result["resultCode"] = 100
        result["resultText"] = "SUCCESS"
        result["content"] = serializer.data
        return JsonResponse(result)


class UserAddressDeleteAPIView(DestroyAPIView):
    serializer_class = UserAddressSerializer
    #permission_classes = (IsAdminUser,)
    #authentication_classes = (TokenAuthentication,)

    def get_queryset(self):
        queryset = Address.objects.filter(user_id=self.request.user.id, id=self.kwargs['pk'])
        return queryset


########################################
#  User Add National ID
########################################


class DriverIDView(APIView):
    def post(self, request, format=None):
        serializer = DriverIDSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

########################################
#  User Add Driver License
########################################


class DriverLicenseView(APIView):
    def post(self, request, format=None):
        serializer = DriverLicenseSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


########################################
#  
########################################


class CarListAPIView(ListAPIView):
    queryset = Car.objects.all()
    serializer_class = CarSerializer

    def list(self, request):
        queryset = self.get_queryset()
        serializer = CarSerializer(queryset, many=True)
        result = {}
        result["resultCode"] = 100
        result["resultText"] = "SUCCESS"
        result["content"] = serializer.data
        return JsonResponse(result)


########################################
#  BOOKING
########################################
class BookingCreateAPIView(CreateAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    #permission_classes = (IsAdminUser,)
    #authentication_classes = (TokenAuthentication,)

    def perform_create(self, serializer):
        print(">>> >>> BookingCreateAPIView CALLED ")
        serializer.save(self.request)
        result = {}
        result["resultCode"] = 100
        result["resultText"] = "SUCCESS"
        result["content"] = serializer.data
        return JsonResponse(result)


class BookingListAPIView(ListAPIView):
    queryset = Booking.objects.all()
    #permission_classes = (IsAdminUser,)
    #authentication_classes = (TokenAuthentication,)

    def list(self, request):
        print(">>> >>> BookingListAPIView CALLED ")
        queryset = self.get_queryset().filter(customer_id=self.request.user.id)
        bookList = []
        for book in queryset:
            bookDic = {}
            bookDic['id'] = book.id
            bookDic['payment_type'] = book.payment_type
            bookDic['driver_rate'] = book.driver_rate
            bookDic['status'] = book.status
            addressQuerySet = Address.objects.all()
            addressQuerySet = addressQuerySet.filter(booking_id=book.id)
            for address in addressQuerySet:
                if address.is_pickup_loc:
                    bookDic['pickup_address_longitude'] = address.longitude
                    bookDic['pickup_address_latitude'] = address.latitude
                    bookDic['pickup_address_description'] = address.description
                elif address.is_arrival_loc:
                    bookDic['arrival_address_longitude'] = address.longitude
                    bookDic['arrival_address_latitude'] = address.latitude
                    bookDic['arrival_address_description'] = address.description

            bookList.append(bookDic.copy())

        result = {}
        result["resultCode"] = 100
        result["resultText"] = "SUCCESS"
        result["content"] = bookList
        return JsonResponse(result)


class BookingCancelAPIView(APIView):
    def get_queryset(self):
        queryset = Booking.objects.filter(customer_id=self.request.user.id, status=0, id=self.request.POST.get('id'))
        return queryset

    def put(self, request, format=None):
        print(">>> >>> BookingCancelAPIView put called")
        bookList = self.get_queryset()
        result = {}
        if bookList.count() == 0:
            result["resultCode"] = 200
            result["resultText"] = "SUCCESS_EMPTY"
            result["content"] = "Book Not Found Error"
        elif bookList.count() > 1:
            result["resultCode"] = 200
            result["resultText"] = "FAILURE"
            result["content"] = "Multiple Book Error"
        else:
            book = bookList.first()
            book.status = 100
            book.save()
            result["resultCode"] = 100
            result["resultText"] = "SUCCESS"
            result["content"] = "Customer's book status was changed to CANCEL"
        return JsonResponse(result)


class BookingSearchDriverAPIView(APIView):
    def get_queryset(self):        
        queryset = Booking.objects.filter(customer_id=self.request.user.id,id=self.request.POST.get('id'))
        return queryset


    def put(self, request, format=None):
        print(">>> >>> BookingSearchDriverAPIView put called")
        bookList = self.get_queryset()
        result = {}
        if bookList.count() == 0:
            result["resultCode"] = 200
            result["resultText"] = "SUCCESS_EMPTY"
            result["content"] = "Book Not Found Error"
        elif bookList.count() > 1:
            result["resultCode"] = 200
            result["resultText"] = "FAILURE"
            result["content"] = "Multiple Book Error"
        else:
            # get book from id 
            book = bookList.first()
            # get book pickup address
            address = Address.objects.filter(is_pickup_loc=1,booking_id=book.id).first()    
            nearestDriverUserInfo = findNearestDriver(address.latitude , address.longitude ,10000)
            book.status = 10
            book.save()
            result["resultCode"] = 100
            result["resultText"] = "SUCCESS"
            result["content"] = { 
                    'userId': nearestDriverUserInfo.user.id ,
                    'driverName' : nearestDriverUserInfo.user.username , 
                    'phone' : nearestDriverUserInfo.phone,
                    'rate' : getDriverPoint()
                }
        return JsonResponse(result)


"""
    Servis sonucunda 'book' tablosunda sürücü update edilmiyor. (Müşteri, sürücüyü kabul etmesi durumunda driver_id set ediliyor )

"""
class BookingAcceptDriverAPIView(APIView):
    def get_queryset(self):        
        queryset = Booking.objects.filter(customer_id=self.request.user.id,id=self.request.POST.get('id'))
        return queryset

    def put(self, request, format=None):
        print(">>> >>> BookingAcceptDriverAPIView put called")
        bookList = self.get_queryset()
        result = {}
        if bookList.count() == 0:
            result["resultCode"] = 200
            result["resultText"] = "SUCCESS_EMPTY"
            result["content"] = "Book Not Found Error"
        elif bookList.count() > 1:
            result["resultCode"] = 200
            result["resultText"] = "FAILURE"
            result["content"] = "Multiple Book Error"
        else:
            # get book from id 
            book = bookList.first()
            # get book pickup address
            result["resultCode"] = 100
            result["resultText"] = "SUCCESS"
            result["content"] = "DENEME"
        return JsonResponse(result)





########################################
# TEST TEST TEST
########################################
class TestCreateAPIView(CreateAPIView):
    queryset = Booking.objects.all()
    serializer_class = TESTSerializer
    #permission_classes = (IsAdminUser,)
    #authentication_classes = (TokenAuthentication,)

    def perform_create(self, serializer):   
        print(">>> >>> TestCreateAPIView CALLED ")
        print(type(serializer))

        serializer.save(user=self.request.user)

        result = {}
        result["resultCode"] = 100
        result["resultText"] = "SUCCESS"
        result["content"] = serializer.data
        return JsonResponse(result)

