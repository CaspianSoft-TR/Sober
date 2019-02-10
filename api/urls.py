from django.urls import path
from django.conf.urls import url
from api import views
from .views import (
    CarListAPIView,
    CarCreateAPIView,
    UserCarCreateAPIView,
    UserCarListAllAPIView,
    UserCarDeleteAPIView,
    DriverIDView,
    DriverLicenseView
)

urlpatterns = [

    path('register/', views.RegisterView.as_view()),

    path('car/create', CarCreateAPIView.as_view() , name='car-add'),
    path('car/', CarListAPIView.as_view() , name='car-list'),

    path('user/car/create', UserCarCreateAPIView.as_view() , name='user-car-add'),
    path('user/car/list-all', UserCarListAllAPIView.as_view() , name='user-car-list-all'),
    path('user/car/delete/<int:pk>/', views.UserCarDeleteAPIView.as_view() , name='user-car-delete'),
    path('user/address/add', views.UserAddressCreateAPIView.as_view() , name='user-address-add'),
    path('user/address/delete/<int:pk>/', views.UserAddressDeleteAPIView.as_view() , name='user-address-delete'),
    path('user/address/list/', views.UserAddressListAPIView.as_view() , name='user-address-list-owner'),
    path('user/address/list-all/', views.UserAddressListAllAPIView.as_view() , name='user-address-list-all'),

    path('driver/add/NaID/', views.DriverIDView.as_view(), name='driver-add-NaID'),
    path('driver/add/DrLicense/', views.DriverLicenseView.as_view(), name='driver-add-DrLicense'),

    path('booking/new', views.BookingCreateAPIView.as_view() , name='booking-new'),
    path('booking/list', views.BookingListAPIView.as_view() , name='booking-new'),
    path('booking/cancel/', views.BookingCancelAPIView.as_view() , name='booking-cancel'),

    path('test', views.TestCreateAPIView.as_view(), name='test'),
]
