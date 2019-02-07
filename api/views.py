
from django.contrib.auth.models import User, Group
from django.contrib.auth.hashers import make_password
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework import viewsets, status
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
    DestroyAPIView
    )

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


class UserAddressDeleteAPIView(DestroyAPIView):
    serializer_class = UserAddressSerializer
    #permission_classes = (IsAdminUser,) 
    #authentication_classes = (TokenAuthentication,) 
    def get_queryset(self):
        queryset = Address.objects.filter(user_id=self.request.user.id, id=self.kwargs['pk'])
        return queryset
















