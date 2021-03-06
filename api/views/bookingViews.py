########################################
#  BOOKING
########################################
from django.contrib.auth.models import User
from django.http import JsonResponse
from rest_framework.decorators import action, permission_classes
from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.views import APIView

from api.permissions import DriverAcceptPermission
from api.utils import utils, notifications, firebase
from api.models import Booking, Address, UserInfo, BookDriver
from api.serializers import CreateBookingSerializer, BookSerializer, UserInfoSerializer
from rest_framework import viewsets

from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly

from api.utils.firebase import Firebase


class BookingCreateAPIView(CreateAPIView):
    queryset = Booking.objects.all()
    serializer_class = CreateBookingSerializer

    # permission_classes = (IsAdminUser,)
    # authentication_classes = (TokenAuthentication,)

    def perform_create(self, serializer):
        serializer.save(self.request)

        # convert to BookSerializer
        book = Booking.objects.get(pk=serializer.data['id'])
        serializer = BookSerializer(book)

        result = {}
        result["resultCode"] = 100
        result["resultText"] = "SUCCESS"
        result["content"] = serializer.data

        return JsonResponse(result)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
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
        if Booking.objects.filter(pk=self.request.POST.get('id')).exists():
            queryset = Booking.objects.get(pk=self.request.POST.get('id'))
            return queryset

    def put(self, request, format=None):
        book = self.get_queryset()
        result = {}
        if not book:
            result["resultCode"] = 200
            result["resultText"] = "SUCCESS_EMPTY"
            result["content"] = "Book Not Found Error"
        else:

            book.status = 100
            book.save()

            # add to improper drivers for the given book
            bookDriver = BookDriver()
            bookDriver.driver = User.objects.get(id=book.driver.id)
            bookDriver.book = book
            bookDriver.save()

            result["resultCode"] = 100
            result["resultText"] = "SUCCESS"
            result["content"] = "Customer's book status was changed to CANCEL"

            # push message body
            messageBody = {
                'book': {
                    'status': 'cancelled',
                    'book_id': book.id,
                }
            }

            # notify driver
            driverUserInfo = UserInfo.objects.get(user_id=book.driver_id)
            if driverUserInfo:
                notifications.send_push_message(driverUserInfo.push_token, 'Sifariş imtina edildi!', messageBody)
        return JsonResponse(result)


class BookingSearchDriverAPIView(APIView):
    def get_queryset(self):
        if Booking.objects.filter(customer_id=self.request.user.id, id=self.request.POST.get('id')).exists():
            queryset = Booking.objects.get(pk=self.request.POST.get('id'))
            return queryset

    def put(self, request, format=None):
        book = self.get_queryset()
        result = {}
        if not book:
            result["resultCode"] = 200
            result["resultText"] = "SUCCESS_EMPTY"
            result["content"] = "Book Not Found Error"
        else:
            # get proper drivers
            properDriverList = utils.findProperDrivers(book.id)

            if properDriverList.count() == 0:
                result["resultCode"] = 200
                result["resultText"] = "SUCCESS_EMPTY"
                result["content"] = "Proper Drivers Not Found"
                return JsonResponse(result)

            # get book pickup address
            pickupAddress = Address.objects.filter(is_pickup_loc=1, booking_id=book.id).first()
            nearestDriverUserInfo = utils.findNearestDriver(pickupAddress.latitude, pickupAddress.longitude, 100000,
                                                            properDriverList)
            book.driver = nearestDriverUserInfo.user
            book.status = 10
            book.save()

            serializer = UserInfoSerializer(nearestDriverUserInfo)
            result["resultCode"] = 100
            result["resultText"] = "SUCCESS"
            result["content"] = serializer.data
            # push message body
            messageBody = {
                'book': {
                    'status': 'new',
                    'book_id': book.id,
                }
            }

            # notify driver
            notifications.send_push_message(nearestDriverUserInfo.push_token, 'Yeni sifariş', messageBody)
        return JsonResponse(result)


"""
    Servis sonucunda 'book' tablosunda sürücü update edilmiyor. (Müşteri, sürücüyü kabul etmesi durumunda driver_id set ediliyor )
"""


class BookingAcceptDriverAPIView(APIView):
    permission_classes = (DriverAcceptPermission,)

    def __init__(self):
        self.firebase = Firebase()

    def get_queryset(self):
        if Booking.objects.filter(id=self.request.POST.get('book_id')).exists():
            queryset = Booking.objects.get(pk=self.request.POST.get('book_id'))
            return queryset

    def put(self, request, format=None):
        book = self.get_queryset()
        self.check_object_permissions(request, book)
        result = {}
        if not book:
            result["resultCode"] = 200
            result["resultText"] = "SUCCESS_EMPTY"
            result["content"] = "Book Not Found Error"
        else:

            customerUserInfo = UserInfo.objects.get(user_id=book.customer.id)
            driverUserInfo = UserInfo.objects.get(user_id=book.driver.id)

            room_id = 'room-' + utils.make_uuid()

            # Driver Accepted Case
            acceptDriver = int(request.POST.get('accept'))
            if acceptDriver == 1:
                book.status = 1
                book.room_id = room_id
                book.save()

                data = {
                    "driver": {
                        "id": driverUserInfo.user_id,
                        "latitude": driverUserInfo.latitude,
                        "longitude": driverUserInfo.longitude
                    },
                    "customer": {
                        "id": customerUserInfo.user_id,
                        "latitude": customerUserInfo.latitude,
                        "longitude": customerUserInfo.longitude
                    }
                }
                self.firebase.create('rooms/' + room_id, data)

                messageBody = {
                    'driver': {
                        'status': 'accepted',
                        'room_id': room_id,
                        'driver_id': driverUserInfo.user.id,
                        'respond': 1
                    }
                }

                # notify customer
                notifications.send_push_message(customerUserInfo.push_token, 'Sifariş qəbul edildi', messageBody)

                result["resultCode"] = 100
                result["resultText"] = "SUCCESS"
                result["content"] = {
                    'tracking_room_id': room_id
                }

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
        if Booking.objects.filter(id=self.request.POST.get('book_id')).exists():
            queryset = Booking.objects.get(pk=self.request.POST.get('book_id'))
            return queryset

    def put(self, request, format=None):
        book = self.get_queryset()
        result = {}
        if not book:
            result["resultCode"] = 200
            result["resultText"] = "SUCCESS_EMPTY"
            result["content"] = "Book Not Found Error"
        else:
            book.setStatusToComplete()
            book.save()
            result["resultCode"] = 100
            result["resultText"] = "SUCCESS"
            result["content"] = {
                'book_status': book.status
            }

            customerUserInfo = UserInfo.objects.get(user_id=book.customer.id)

            messageBody = {
                'driver': {
                    'status': 'completed',
                    'driver_id': book.driver.id,
                    'respond': 200
                }
            }

            # notify customer
            notifications.send_push_message(customerUserInfo.push_token, 'Sürüş bitdi', messageBody)
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
    permission_classes = (IsAuthenticatedOrReadOnly,)
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

    @action(methods=['post'], detail=True, permission_classes=[IsAuthenticated], url_path='arrived')
    def arrived(self, request, pk=None):
        book = Booking.objects.get(pk=pk)
        book.status = 20
        book.save()
        serializer = BookSerializer(book)

        # get customer detail
        customer = UserInfo.objects.get(user_id=book.customer.id)

        messageBody = {
            'driver': {
                'status': 'arrived',
                'driver_id': book.driver.id,
                'respond': 20
            }
        }

        # notify customer
        notifications.send_push_message(customer.push_token, 'Sürücü sizi gözləyir', messageBody)

        return JsonResponse(serializer.data)
