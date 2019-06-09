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

from django.contrib import admin
from django.urls import path
from django.conf.urls import url, include
from rest_framework.documentation import include_docs_urls
from rest_framework import routers
from rest_framework_jwt.views import obtain_jwt_token

from api.views.mainViews import RegisterView
from django.conf import settings
from django.conf.urls.static import static

router = routers.DefaultRouter()
# router.register(r'users', views.UserViewSet)

API_TITLE = 'Taxi Booking API'
API_DESCRIPTION = 'API for Taxi Booking'

urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^', include(router.urls)),

    # url(r'^node_api$', 'api.views.node_api', name='node_api'),

    # MAIN DIRECTORY
    url(r'^docs/', include_docs_urls(title=API_TITLE, description=API_DESCRIPTION)),
    path('api/v1/', include('api.urls')),
    path('api-auth/', include('rest_framework.urls')),

    # REST-AUTH DIRECTORIES
    path('rest-auth/', include('rest_auth.urls')),
    path('rest-auth/registration/', include('rest_auth.registration.urls')),

    #  CUSTOM REGISTER DIRECTORY - it will remove
    url(r'^rest-auth/register/create/$', RegisterView.as_view(), name='custom-register'),
    path('', include('drfpasswordless.urls')),

    # JWT login
    url(r'^oauth/token', obtain_jwt_token),

]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
