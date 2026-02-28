from djoser.serializers import UserSerializer as BaseUserSerializer , UserCreateSerializer as BaseUserCreateSerializer
from rest_framework import serializers

#Responsible creating a User and Customer
class UserCreateSerializer(BaseUserCreateSerializer):
    class Meta(BaseUserCreateSerializer.Meta):
        fields = ['id' , 'username', 'password',
                  'email' , 'first_name' , 'last_name']

class UserSerializer(BaseUserSerializer):
    class Meta(BaseUserSerializer.Meta):
        fields = ['id' , 'username' , 'email' , 'first_name' , 'last_name']
