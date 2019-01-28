
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
    CreateAPIView 
    )

from rest_auth.registration.views import RegisterView
from . import models
from . import serializers
from api.serializers import *


class RegisterView(RegisterView):
    def get_serializer_class(self):
        return serializers.RegisterSerializer


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
        result = {}
        result["resultCode"] = 100;
        result["resultText"] = "SUCCESS";
        result["content"] = serializer.data
        return JsonResponse(result)










'''
# CAR LIST
@csrf_exempt
def car_operations(request):
    result = {}
    #if not request.user.is_staff or not request.user.is_superuser: 
    #    result["resultCode"] = 201;
    #    result["resultText"] = "FAILURE_AUTH";
    #    result["content"] = status.HTTP_400_BAD_REQUEST;
    #    return JsonResponse(result, safe=False) 

    if request.method == 'GET':

        cars = Car.objects.all()
        if cars.count() == 0:
            result["resultCode"] = 101;
            result["resultText"] = "SUCCESS_EMPTY"
            result["content"] = "Car list size is 0"

        else:
            result["resultCode"] = 100;
            result["resultText"] = "SUCCESS";
            serializer = CarSerializer(cars, many=True)
            result["content"] = serializer.data

        #print(type(cars))
        return JsonResponse(result, safe=False)

    elif request.method == 'POST':
        print(type(request))
        print(type(request.POST))

        #mutable = request.POST._mutable
        #request.POST._mutable = True
        #request.POST['added_by_id'] = 1
        #request.POST._mutable = mutable

        serializer = CarSerializer(data=request.POST)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


#@api_view(['GET', 'POST', 'DELETE'])
@csrf_exempt
def car_detail(request, pk):
    try:
        car = Car.objects.get(pk=pk)
    except Car.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = CarSerializer(car)
        return JsonResponse(serializer.data)

    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = CarSerializer(car, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=400)

    elif request.method == 'DELETE':
        car.delete()
        return HttpResponse(status=204)



class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


@csrf_exempt
def user_register(request):

    if request.method == 'GET':
        user = User.objects.all()
        serializer = UserSerializer(user, many=True)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'POST':
        result = {}
        result["resultCode"] = 101
        result["resultText"] = "SUCCESS"
        print(request.POST.get("username", ""))
        print(request.POST.get("email", ""))
        serializer = UserSerializer(data=request.POST)
        if serializer.is_valid():
            serializer.save()
            #userProfileSerializer = UserInfoSerializer(data=request.POST)
            # if userProfileSerializer.is_valid():
            #    userProfileSerializer.save()
            result["resultCode"] = 101
            result["resultText"] = "SUCCESS"
            result["content"] = serializer.data
            return JsonResponse(result, status=status.HTTP_201_CREATED)

        #result["resultCode"] = 201;
        #result["resultText"] = "FAILURE";
        #result["content"] = serializer.errors;
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

'''