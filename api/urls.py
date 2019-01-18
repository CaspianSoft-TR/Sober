from django.urls import path

from api import views

urlpatterns = [
    path('car/', views.car_list),
    path('car/<int:pk>/', views.car_detail),
    path('user/register/', views.user_register),
]