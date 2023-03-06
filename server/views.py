from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny
from django.contrib.auth import authenticate
from rest_framework import viewsets

from .models import Room
from .serializers import UserSerializer, TokenSerializer, RoomSerializer


class RegisterView(APIView): #Метод для обработки регистрации
    permission_classes = (AllowAny,)

    @staticmethod
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token, created = Token.objects.get_or_create(user=user)
            token_serializer = TokenSerializer(token)
            return Response(token_serializer.data)
        return Response(serializer.errors)


class LoginView(APIView): #Метод для обработки входа
    permission_classes = (AllowAny,)

    @staticmethod
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(request, username=username, password=password)

        if user:
            token, created = Token.objects.get_or_create(user=user)
            token_serializer = TokenSerializer(token)
            return Response(token_serializer.data)
        return Response({'error': 'Invalid credentials'})


class RoomViewSet(viewsets.ModelViewSet):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer