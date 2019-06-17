from django.db.models import Q
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


class CustomerViewSet(viewsets.ViewSet):
    permission_classes = (IsAuthenticatedOrReadOnly,)

    """
    A simple ViewSet for listing or retrieving users.
    """

    def retrieve(self, request, pk=None):
        customer = UserInfo.objects.filter(user_id=pk, is_customer=1).first()
        serializer = UserInfoSerializer(customer)
        response = {
            'resultCode': 100,
            'resultText': 'SUCCESS',
            'content': serializer.data
        }
        return JsonResponse(response)

    def list(self, request):
        customers = UserInfo.objects.filter(is_customer=1).all()
        serializer = UserInfoSerializer(customers, many=True)
        response = {
            'resultCode': 100,
            'resultText': 'SUCCESS',
            'content': serializer.data
        }
        return JsonResponse(response)

    @action(methods=['get'], detail=True, permission_classes=[IsAuthenticated], url_path='on-way')
    def on_the_way(self, request, pk=None):
        book = Booking.objects.filter(status=20, customer_id=request.user.id).last()
        if book is None:
            response = {
                'resultCode': 200,
                'resultText': 'SUCCESS_EMPTY',
                'content': "Book not found!"
            }
            return JsonResponse(response)

        serializer = BookSerializer(book)
        response = {
            'resultCode': 100,
            'resultText': 'SUCCESS',
            'content': serializer.data
        }
        return JsonResponse(response)

    @action(methods=['get'], detail=True, permission_classes=[IsAuthenticated], url_path='has-tracking')
    def tracking(self, request, pk=None):
        book = Booking.objects.filter(customer_id=request.user.id, status=1).first()
        if book is None:
            response = {
                'resultCode': 200,
                'resultText': 'SUCCESS_EMPTY',
                'content': "No tracking book found!"
            }
            return JsonResponse(response)

        serializer = BookSerializer(book)
        response = {
            'resultCode': 100,
            'resultText': 'SUCCESS',
            'content': serializer.data
        }
        return JsonResponse(response)

    @action(methods=['get'], detail=True, permission_classes=[IsAuthenticated], url_path='history')
    def tracking(self, request, pk=None):
        books = Booking.objects.filter(Q(status='200') | Q(status='100'), customer_id=request.user.id).all()
        if books.count() == 0:
            response = {
                'resultCode': 200,
                'resultText': 'SUCCESS_EMPTY',
                'content': "Book not found!"
            }
            return JsonResponse(response)

        serializer = BookSerializer(books, many=True)
        response = {
            'resultCode': 100,
            'resultText': 'SUCCESS',
            'content': serializer.data
        }
        return JsonResponse(response)
