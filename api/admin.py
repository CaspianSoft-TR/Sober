from django.contrib import admin
#from api.models import *

# Register your models here.
from api.models import Booking, UserInfo, UserCar, Car

admin.site.register(Booking)
admin.site.register(UserInfo)
admin.site.register(Car)
admin.site.register(UserCar)