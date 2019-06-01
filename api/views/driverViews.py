from django.http import JsonResponse
from rest_auth.serializers import UserDetailsSerializer
from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView

from api.models import UserInfo
from api.serializers import DriverIDSerializer, DriverLicenseSerializer, UserInfoSerializer


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


class DriverViewSet(viewsets.ViewSet):
    # permission_classes = (IsAuthenticated,)
    # serializer_class = BookSerializer

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
