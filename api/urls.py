from django.urls import path
from django.conf.urls import url
from api import views
from .views import (
	CarListAPIView,
	CarCreateAPIView,
    UserCarCreateAPIView,
    UserCarListAllAPIView,
    UserCarDeleteAPIView
	)

urlpatterns = [

    #url(r'^$', CustomRegistrationView.as_view(), name='rest_register'),
    #path('user/register/', views.user_register),
    #path('reg/', views.CustomRegistrationView.as_view()),
    #path('car/<int:pk>/', views.car_detail),
    #path('car/', views.car_operations),

    path('car/create', CarCreateAPIView.as_view() , name='car-add'),
    path('car/', CarListAPIView.as_view() , name='car-list'),
    path('register/', views.RegisterView.as_view()),


    path('user/car/create', UserCarCreateAPIView.as_view() , name='user-car-add'),
    path('user/car/list-all', UserCarListAllAPIView.as_view() , name='user-car-list-all'),
    path('user/car/delete/<int:pk>/', views.UserCarDeleteAPIView.as_view() , name='user-car-delete'),
    path('user/address/add', views.UserAddressCreateAPIView.as_view() , name='user-address-add'),
    path('user/address/delete/<int:pk>/', views.UserAddressDeleteAPIView.as_view() , name='user-address-delete'),
    path('user/address/list/', views.UserAddressListAPIView.as_view() , name='user-address-list-owner'),
    path('user/address/list-all/', views.UserAddressListAllAPIView.as_view() , name='user-address-list-all'),
]
