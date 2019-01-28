from django.urls import path
from django.conf.urls import url
from api import views
from .views import (
	CarListAPIView,
	CarCreateAPIView
	)

urlpatterns = [

    #url(r'^$', CustomRegistrationView.as_view(), name='rest_register'),
    #path('user/register/', views.user_register),
    #path('reg/', views.CustomRegistrationView.as_view()),
    #path('car/<int:pk>/', views.car_detail),
    #path('car/', views.car_operations),
    
    path('car/create', CarCreateAPIView.as_view() , name='car-add'),
    path('car/', CarListAPIView.as_view() , name='car-list'),
    path('reg', views.RegisterView.as_view()),
]
