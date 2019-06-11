from django.http import JsonResponse
from rest_framework import status, viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import action
from rest_framework.parsers import FileUploadParser
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from api.permissions import IsLoggedInUserOrAdmin

from api.models import UserInfo, Document, Booking
from api.serializers import DriverIDSerializer, DriverLicenseSerializer, UserInfoSerializer, BookSerializer


class DriverIDView(APIView):
    parser_class = (FileUploadParser,)

    def post(self, request, *args, **kwargs):
        user = request.user
        driver_exists = Document.objects.filter(user_id=user.id).exists()
        if driver_exists is False:
            file_serializer = DriverIDSerializer(data=request.data)
            file_serializer.is_valid()
            file_serializer.save(user=request.user)
            return Response(file_serializer.data, status=status.HTTP_201_CREATED)
        else:
            driver = Document.objects.filter(user_id=user.id).first()
            file_serializer = DriverIDSerializer(driver, data=request.data)
            file_serializer.is_valid()
            file_serializer.save(user=request.user)
            return Response(file_serializer.data, status=status.HTTP_202_ACCEPTED)


########################################
#  User Add Driver License
########################################


class DriverLicenseView(APIView):
    parser_class = (FileUploadParser,)

    def post(self, request, *args, **kwargs):
        user = request.user
        driver_exists = Document.objects.filter(user_id=user.id).exists()
        if driver_exists is False:
            file_serializer = DriverLicenseSerializer(data=request.data)
            file_serializer.is_valid()
            file_serializer.save(user=request.user)
            return Response(file_serializer.data, status=status.HTTP_201_CREATED)
        else:
            driver = Document.objects.filter(user_id=user.id).first()
            file_serializer = DriverLicenseSerializer(driver, data=request.data)
            file_serializer.is_valid()
            file_serializer.save(user=request.user)
            return Response(file_serializer.data, status=status.HTTP_202_ACCEPTED)


class DriverViewSet(viewsets.ViewSet):
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

    @action(methods=['get'], detail=True, permission_classes=[IsAuthenticated], url_path='has-book')
    def has_new_book(self, request, pk=None):
        book = Booking.objects.filter(status=10, driver_id=request.user.id).last()
        if book is None:
            response = {
                'resultCode': 200,
                'resultText': 'SUCCESS_EMPTY',
                'content': "No new book found!"
            }
            return JsonResponse(response)

        serializer = BookSerializer(book)
        response = {
            'resultCode': 100,
            'resultText': 'SUCCESS',
            'content': serializer.data
        }
        return JsonResponse(response)
