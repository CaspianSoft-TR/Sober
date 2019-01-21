"""sober URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
'''
from django.contrib import admin
from django.urls import include, path
from django.conf.urls import url, include
from django.contrib.auth.models import User
from rest_framework import routers, serializers, viewsets
from api import views

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'groups', views.GroupViewSet)


urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('api/', include('api.urls')),
]
'''

from django.contrib import admin
from django.urls import include, path
from django.conf.urls import url, include
from rest_framework.documentation import include_docs_urls
from rest_framework import routers, serializers, viewsets
from api import views
from api.views import RegisterView

router = routers.DefaultRouter()
#router.register(r'users', views.UserViewSet)
#router.register(r'groups', views.GroupViewSet)

API_TITLE = 'Taxi Booking API'
API_DESCRIPTION = 'API for Taxi Booking'

urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^', include(router.urls)),
    path('api/v1/', include('api.urls')),
    path('api-auth/', include('rest_framework.urls')),


    path('rest-auth/', include('rest_auth.urls')),
    path('rest-auth/registration/', include('rest_auth.registration.urls')),

    url(r'^rest-auth/register/create/$', RegisterView.as_view(), name='custom-register'),
    url(r'^docs/', include_docs_urls(title=API_TITLE, description=API_DESCRIPTION)),
]
