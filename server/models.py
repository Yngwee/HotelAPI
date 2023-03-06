from django.db import models
from django.contrib.auth.models import AbstractUser


# class User(AbstractUser):
#     pass

class User(models.Model):
    username = models.CharField(max_length=30)
    email = models.CharField(max_length=50)
    login = models.CharField(max_length=30)
    password = models.CharField(max_length=30)
    last_login = models.DateTimeField(blank=True, null=True)

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username


class Token(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    key = models.CharField(max_length=40, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)


class Room(models.Model):
    number = models.CharField('Номер комнаты', max_length=30, unique=True)
    price = models.IntegerField('Цена')
    capacity = models.IntegerField('Количество мест')
    description = models.TextField('Описание комнаты', max_length=500, null=True, blank=True)

    class Meta:
        verbose_name = 'Комната'
        verbose_name_plural = 'Комнаты'
    def __str__(self):
        return self.number



class UserProfile(models.Model):
    userId = models.OneToOneField(User, on_delete=models.CASCADE)
    bookedRoomId = models.ForeignKey(Room, on_delete=models.CASCADE)
    bookedDate = models.DurationField()
