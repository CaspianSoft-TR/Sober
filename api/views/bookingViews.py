########################################
#  BOOKING
########################################
from django.contrib.auth.models import User
from django.http import JsonResponse, Http404
from rest_framework.generics import CreateAPIView, ListAPIView, get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet

from api import utils, notifications
from api.models import Booking, Address, UserInfo, BookDriver
from api.serializers import BookingSerializer, BookSerializer
from rest_framework import status, mixins, permissions, viewsets


class BookingCreateAPIView(CreateAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer

    # permission_classes = (IsAdminUser,)
    # authentication_classes = (TokenAuthentication,)

    def perform_create(self, serializer):
        print(">>> >>> BookingCreateAPIView CALLED ")
        serializer.save(self.request)
        result = {}
        result["resultCode"] = 100
        result["resultText"] = "SUCCESS"
        result["content"] = serializer.data
        return JsonResponse(result)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        # headers = self.get_success_headers(serializer.data)
        # return Response({'Message': 'You have successfully register'}, status=status.HTTP_201_CREATED, headers=headers)
        return self.perform_create(serializer)


class BookingListAPIView(ListAPIView):
    queryset = Booking.objects.all()

    # permission_classes = (IsAdminUser,)
    # authentication_classes = (TokenAuthentication,)

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
        queryset = Booking.objects.filter(customer_id=self.request.user.id, id=self.request.POST.get('id'))
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
            properDriverList = utils.findProperDrivers(book.id)
            print('properDriverList', properDriverList.count())

            if properDriverList.count() == 0:
                result["resultCode"] = 200
                result["resultText"] = "SUCCESS_EMPTY"
                result["content"] = "Proper Drivers Not Found"
                return JsonResponse(result)

            pickupAddress = Address.objects.filter(is_pickup_loc=1, booking_id=book.id).first()
            dropOffAddress = Address.objects.filter(is_pickup_loc=0, booking_id=book.id).first()

            nearestDriverUserInfo = utils.findNearestDriver(pickupAddress.latitude, pickupAddress.longitude, 100000,
                                                            properDriverList)

            book.driver = nearestDriverUserInfo.user
            book.status = 10
            book.save()
            result["resultCode"] = 100
            result["resultText"] = "SUCCESS"
            result["content"] = {
                'userId': nearestDriverUserInfo.user.id,
                'driverName': nearestDriverUserInfo.user.username,
                'latitude': nearestDriverUserInfo.latitude,
                'longitude': nearestDriverUserInfo.longitude,
                'phone': nearestDriverUserInfo.phone,
                'rate': utils.getDriverPoint()
            }
            # push token body
            messageBody = {
                'book': {
                    'status': 'new',
                    'book_id': book.id,
                }
            }

            # send message by firebase
            # firebaseResult = utils.send_message(nearestDriverUserInfo.firebase_token, "new_book", messageBody)

            notifications.send_push_message(nearestDriverUserInfo.push_token, 'Yeni sifariş', messageBody)
            print("--------------- FIREBASE NOTIFICATION ---------------")

        return JsonResponse(result)


"""
    Servis sonucunda 'book' tablosunda sürücü update edilmiyor. (Müşteri, sürücüyü kabul etmesi durumunda driver_id set ediliyor )
"""


class BookingAcceptDriverAPIView(APIView):
    def get_queryset(self):
        queryset = Booking.objects.filter(driver_id=self.request.user.id, id=self.request.POST.get('book_id'))
        return queryset

    def put(self, request, format=None):
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
            customerUserInfo = UserInfo.objects.get(user_id=book.customer.id)
            driverUserInfo = UserInfo.objects.get(user_id=book.driver.id)

            # Driver Accepted Case
            acceptDriver = int(request.POST.get('accept'))
            if acceptDriver == 1:
                book.status = 1

                messageBody = {
                    'driver': {
                        'status': 'accepted',
                        'driver_id': driverUserInfo.user.id,
                        'respond': 1
                    }
                }

                # notify customer
                notifications.send_push_message(customerUserInfo.push_token, 'Sifariş qəbul edildi', messageBody)

                book.save()

                result["resultCode"] = 100
                result["resultText"] = "SUCCESS"
                result["content"] = "Trip started..."

            # -3- Driver Rejected Case
            else:
                # -3.1-
                book.status = 2
                book.save()

                # -3.2-
                bookDriver = BookDriver()
                bookDriver.driver = User.objects.get(id=book.driver.id)
                bookDriver.book = book
                bookDriver.save()

                messageBody = {
                    'driver': {
                        'status': 'rejected',
                        'driver_id': driverUserInfo.user.id,
                        'respond': 2
                    }
                }

                # notify customer
                notifications.send_push_message(customerUserInfo.push_token, 'Sifariş qəbul olunmadı', messageBody)

                result["resultCode"] = 100
                result["resultText"] = "REJECTED"
                result["content"] = "Book Rejected"

        return JsonResponse(result)


# "book_id" her ne kadar gerekmese de veritabanında kontrol amacıyla konulmuştur
class BookingCompletedAPIView(APIView):
    def get_queryset(self):
        queryset = Booking.objects.filter(driver_id=self.request.user.id, id=self.request.POST.get('book_id'), status=1)
        return queryset

    def put(self, request, format=None):
        print(">>> >>> BookingCompletedAPIView put called")
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
            book.setStatusToComplete()
            book.save()
            result["resultCode"] = 100
            result["resultText"] = "SUCCESS"
            result["content"] = {
                'book_status': book.status
            }
        return JsonResponse(result)


# "book_id" her ne kadar gerekmese de veritabanında kontrol amacıyla konulmuştur
class BookingDriverRateAPIView(APIView):
    def get_queryset(self):
        queryset = Booking.objects.filter(customer_id=self.request.user.id, id=self.request.POST.get('book_id'),
                                          status=200)
        return queryset

    #  update driver rate
    def post(self, request, format=None):
        print(">>> >>> BookingDriverRateAPIView put called")
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
            if book.driver_rate == 0:

                if int(self.request.POST.get('rate')) > 5:
                    book.driver_rate = 5
                elif int(self.request.POST.get('rate')) < 1:
                    book.driver_rate = 1
                else:
                    book.driver_rate = int(self.request.POST.get('rate'))

                book.save()
                result["resultCode"] = 100
                result["resultText"] = "SUCCESS"
                result["content"] = {
                    'book_status': 'update driver rate'
                }
            else:
                result["resultCode"] = 200
                result["resultText"] = "FAILURE"
                result["content"] = {
                    'desc': 'Cant rate multiple times'
                }
        return JsonResponse(result)


class BookViewSet(viewsets.ViewSet):
    # permission_classes = (IsAuthenticated,)
    # serializer_class = BookSerializer

    """
    A simple ViewSet for listing or retrieving users.
    """

    def retrieve(self, request, pk=None):
        book = Booking.objects.get(pk=pk)
        serializer = BookSerializer(book)
        response = {
            'resultCode': 100,
            'resultText': 'SUCCESS',
            'content': serializer.data
        }
        return JsonResponse(response)

    def list(self, request):
        books = Booking.objects.all()
        serializer = BookSerializer(books, many=True)
        response = {
            'resultCode': 100,
            'resultText': 'SUCCESS',
            'content': serializer.data
        }
        return JsonResponse(response)
