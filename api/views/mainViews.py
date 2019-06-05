
from django.http import JsonResponse
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.generics import (
    ListAPIView,
    CreateAPIView,
    DestroyAPIView,
)
from rest_framework.views import APIView
from rest_auth.registration.views import (
    RegisterView,
)
from api.serializers import *
from api.models import *

from api.utils import notifications


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


class UserFirebaseTokenUpdateAPIView(APIView):
    def get_queryset(self):
        queryset = UserInfo.objects.filter(user=self.request.user.id)
        return queryset

    def put(self, request, format=None):
        print(">>> >>> UserFirebaseTokenUpdateAPIView put called")
        userInfo = self.get_queryset()
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
            userProfile.firebase_token = self.request.POST.get('token')
            userProfile.save()
            result["resultCode"] = 100
            result["resultText"] = "SUCCESS"
            result["content"] = "User token updated"
        
        return JsonResponse(result)


class UpdateUserPushTokenAPIView(APIView):
    def get_queryset(self):
        queryset = UserInfo.objects.filter(user=self.request.user.id)
        return queryset

    def put(self, request, format=None):
        print(">>> >>> UserPushTokenUpdateAPIView put called")
        userInfo = self.get_queryset()
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
            userProfile.push_token = self.request.POST.get('token')
            userProfile.save()
            result["resultCode"] = 100
            result["resultText"] = "SUCCESS"
            result["content"] = "User token updated"
        
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
        result["content"] = serializer
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

class SendPushNotificationView(APIView):
    def post(self, request):
        token = request.data.get('pushToken')
        notifications.send_push_message(token, 'hello orxan')
        return Response({'token': token})