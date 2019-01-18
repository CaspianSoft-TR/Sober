from django.contrib.auth.models import User, Group
from rest_framework import serializers
from api.models import UserInfo,Car


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'groups')


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ('url', 'name')


class UserInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserInfo
        fields = ('phone')

class CarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Car
        fields = ('car_brand', 'number_plate', 'color')


