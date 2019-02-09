
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


class RegisterView(RegisterView):
    def get_serializer_class(self):
        return RegisterSerializer


class CarListAPIView(ListAPIView):
    queryset = Car.objects.all()
    serializer_class = CarSerializer
    def list(self, request):
        queryset = self.get_queryset()
        serializer = CarSerializer(queryset, many=True)
        result = {}
        result["resultCode"] = 100;
        result["resultText"] = "SUCCESS";
        result["content"] = serializer.data
        return JsonResponse(result)


class CarCreateAPIView(CreateAPIView):
    queryset = Car.objects.all()
    serializer_class = CarSerializer
    permission_classes = (IsAdminUser,) 
    authentication_classes = (TokenAuthentication,) 
    def perform_create(self, serializer):
        serializer.save(added_by=self.request.user)
        #aşağıdaki degerleri return etmesi gerekir
        result = {}
        result["resultCode"] = 100;
        result["resultText"] = "SUCCESS";
        result["content"] = serializer.data
        return JsonResponse(result)


########################################
########## USERCAR 
########################################
class UserCarCreateAPIView(CreateAPIView):
    queryset = UserCar.objects.all()
    serializer_class = UserCarSerializer
    #permission_classes = (IsAdminUser,) 
    #authentication_classes = (TokenAuthentication,) 
    def perform_create(self, serializer):
        #carId = Car.objects.get(id=serializer.validated_data['car_idx'])
        #print(serializer.validated_data['car_idx'])

        serializer.save(user=self.request.user)
        print(">>> >>> UserCarCreateAPIView CALLED ")
        result = {}
        result["resultCode"] = 100;
        result["resultText"] = "SUCCESS";
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
        result["resultCode"] = 100;
        result["resultText"] = "SUCCESS";
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
########## USER ADDRESS
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
        result["resultCode"] = 100;
        result["resultText"] = "SUCCESS";
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
        result["resultCode"] = 100;
        result["resultText"] = "SUCCESS";
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
        result["resultCode"] = 100;
        result["resultText"] = "SUCCESS";
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
########## BOOKING
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
        result["resultCode"] = 100;
        result["resultText"] = "SUCCESS";
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
        result["resultCode"] = 100;
        result["resultText"] = "SUCCESS";
        result["content"] = bookList
        return JsonResponse(result)



class BookingCancelAPIView(APIView):
    def get_queryset(self):
        queryset = Booking.objects.filter(customer_id=self.request.user.id, status=0,id=self.request.POST.get('id'))
        return queryset
    
    def put(self, request, format=None):
        print(">>> >>> BookingCancelAPIView put called")
        bookList = self.get_queryset()
        result = {}
        if bookList.count() == 0:
            result["resultCode"] = 200;
            result["resultText"] = "SUCCESS_EMPTY";
            result["content"] = "Book Not Found Error"
        elif bookList.count() > 1:
            result["resultCode"] = 200;
            result["resultText"] = "FAILURE";
            result["content"] = "Multiple Book Error"
        else:
            book = bookList.first()
            book.status = 100
            book.save()
            result["resultCode"] = 100;
            result["resultText"] = "SUCCESS";
            result["content"] = "Customer's book status was changed to CANCEL"
        return JsonResponse(result)


########################################
########## TEST TEST TEST 
########################################
class TestCreateAPIView(CreateAPIView):
    queryset = Booking.objects.all()
    serializer_class = TESTSerializer
    #permission_classes = (IsAdminUser,) 
    #authentication_classes = (TokenAuthentication,) 
    def perform_create(self, serializer):
        print(">>> >>> TestCreateAPIView CALLED ")
        print( type(serializer) )

        serializer.save(user=self.request.user)

        result = {}
        result["resultCode"] = 100;
        result["resultText"] = "SUCCESS";
        result["content"] = serializer.data
        return JsonResponse(result)
















