from django.db import models


class User(models.Model):
    name = models.CharField(max_length=30)
    mail = models.CharField(max_length=50)
    login = models.CharField(max_length=30)
    password = models.CharField(max_length=30)

class Room(models.Model):
    number = models.CharField(max_length=30)
    price = models.FloatField()
    capacity = models.IntegerField()

class UserProfile(models.Model):
    userId = models.OneToOneField(User, on_delete=models.CASCADE)
    bookedRoomId = models.ForeignKey(Room, on_delete=models.CASCADE)
    bookedDate = models.DurationField()
