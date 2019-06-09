from django.http import JsonResponse
from rest_framework import status, viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.parsers import FileUploadParser
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.views import APIView

from django.conf import settings
import os

from api.models import UserInfo, Driver
from api.serializers import DriverIDSerializer, DriverLicenseSerializer, UserInfoSerializer


class DriverIDView(APIView):
    parser_class = (FileUploadParser,)

    def post(self, request, *args, **kwargs):
        user = request.user
        driver_exists = Driver.objects.filter(user_id=user.id).exists()
        if driver_exists is False:
            file_serializer = DriverIDSerializer(data=request.data)
            file_serializer.is_valid()
            file_serializer.save(user=request.user)
            return Response(file_serializer.data, status=status.HTTP_201_CREATED)
        else:
            driver = Driver.objects.filter(user_id=user.id).first()
            file_serializer = DriverIDSerializer(driver, data=request.data)
            file_serializer.is_valid()
            file_serializer.save(user=request.user)
            return Response(file_serializer.data, status=status.HTTP_202_ACCEPTED)


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


class DriverViewSet(viewsets.ViewSet):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticatedOrReadOnly,)

    """
    A simple ViewSet for listing or retrieving users.
    """

    def retrieve(self, request, pk=None):
        driver = UserInfo.objects.filter(user_id=pk, is_driver=1).first()
        serializer = UserInfoSerializer(driver)
        response = {
            'resultCode': 100,
            'resultText': 'SUCCESS',
            'content': serializer.data
        }
        return JsonResponse(response)

    def list(self, request):
        drivers = UserInfo.objects.filter(is_driver=1).all()
        serializer = UserInfoSerializer(drivers, many=True)
        response = {
            'resultCode': 100,
            'resultText': 'SUCCESS',
            'content': serializer.data
        }
        return JsonResponse(response)
