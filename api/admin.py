from django.contrib import admin
# from api.models import *

# Register your models here.
from django.contrib.auth.models import User

from api.models import Booking, UserInfo, UserCar, Car
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import ugettext_lazy as _

admin.site.register(Booking)
admin.site.register(Car)
admin.site.register(UserCar)


class UserInfoInline(admin.StackedInline):
    model = UserInfo
    can_delete = False


class UserAdmin(BaseUserAdmin):
    fieldsets = (
        (_('Personal Info'),
         {'fields': ('email', 'first_name', 'last_name', 'is_staff', 'is_active', 'is_superuser', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff')
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('email',)
    inlines = (UserInfoInline,)


admin.site.unregister(User)  # First unregister the old class
admin.site.register(User, UserAdmin)
