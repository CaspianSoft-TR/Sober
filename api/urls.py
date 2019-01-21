from django.urls import path
from django.conf.urls import url
from api import views

urlpatterns = [
    #url(r'^$', CustomRegistrationView.as_view(), name='rest_register'),
    # path('car/', views.car_list),
    #path('reg/', views.CustomRegistrationView.as_view()),
    # path('car/<int:pk>/', views.car_detail),
    # path('user/register/', views.user_register),
    path('reg', views.RegisterView.as_view()),
]
