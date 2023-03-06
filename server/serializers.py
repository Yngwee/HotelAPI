from rest_framework import serializers
from .models import User, Token
from .models import Room


from rest_framework import serializers
from .models import User, Token

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

class TokenSerializer(serializers.ModelSerializer): #Сериалайзер для токена
    class Meta:
        model = Token
        fields = ('key',)


class RoomSerializer(serializers.ModelSerializer): #Сериалайзер для комнат
    class Meta:
        model = Room
        fields = ('number', 'price', 'capacity')

class FilterSerializer(serializers.ModelSerializer):
    class Meta:
        pass