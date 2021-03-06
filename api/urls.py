from django.conf.urls import url, include
from django.urls import path
from rest_framework.routers import DefaultRouter

from api import views
from api.views import BookViewSet, DriverViewSet, UserViewSet, CustomerViewSet
from api.views.mainViews import (
    CarListAPIView,
    CarCreateAPIView,
    UserCarCreateAPIView,
    UserCarListAllAPIView,
)

router = DefaultRouter()
# Define API RESOURCES
router.register(r'books', BookViewSet, basename='book')
router.register(r'drivers', DriverViewSet, basename='driver')
router.register(r'customers', CustomerViewSet, basename='customer')
router.register(r'users', UserViewSet)

# router.register(r'addresses', AccountViewSet)

urlpatterns = [

    url(r'^auth/', include('rest_auth.urls')),
    url(r'^register/', views.RegisterView.as_view()),

    path('car/create', CarCreateAPIView.as_view(), name='car-add'),
    path('car/', CarListAPIView.as_view(), name='car-list'),

    path('user/car/create', UserCarCreateAPIView.as_view(), name='user-car-add'),
    path('user/car/list-all', UserCarListAllAPIView.as_view(), name='user-car-list-all'),
    path('user/car/delete/<int:pk>/', views.UserCarDeleteAPIView.as_view(), name='user-car-delete'),
    path('user/address/add', views.UserAddressCreateAPIView.as_view(), name='user-address-add'),
    path('user/address/delete/<int:pk>/', views.UserAddressDeleteAPIView.as_view(), name='user-address-delete'),
    path('user/address/list/', views.UserAddressListAPIView.as_view(), name='user-address-list-owner'),
    path('user/address/list-all/', views.UserAddressListAllAPIView.as_view(), name='user-address-list-all'),
    path('user/book/accept-user/', views.BookingAcceptDriverAPIView.as_view(), name='user-book-accept-driver'),
    path('user/location/set/', views.UserLocationUpdateAPIView.as_view(), name='user-profile-set-location'),
    path('user/update/firebase-token/', views.UserFirebaseTokenUpdateAPIView.as_view(), name='user-firebase-token-set'),

    path('driver/add/NaID/', views.DriverIDView.as_view(), name='driver-add-NaID'),
    path('driver/add/DrLicense/', views.DriverLicenseView.as_view(), name='driver-add-DrLicense'),

    path('booking/new', views.BookingCreateAPIView.as_view(), name='booking-new'),
    path('booking/list', views.BookingListAPIView.as_view(), name='booking-list'),
    path('booking/cancel/', views.BookingCancelAPIView.as_view(), name='booking-cancel'),
    path('booking/search-driver/', views.BookingSearchDriverAPIView.as_view(), name='booking-search-driver'),
    path('booking/<int:book_id>/arrived', BookViewSet.as_view({"post": "arrived"}), name='booking-driver-arrived'),
    path('booking/completed/', views.BookingCompletedAPIView.as_view(), name='booking-completed'),
    path('booking/driver/rate/', views.BookingDriverRateAPIView.as_view(), name='booking-driver-rate'),

    path('test', views.TestCreateAPIView.as_view(), name='test'),

    path('notify', views.SendPushNotificationView.as_view(), name='SendPushNotificationView'),
    path('push-token', views.UpdateUserPushTokenAPIView.as_view(), name='update-push-token'),
]

urlpatterns += router.urls
