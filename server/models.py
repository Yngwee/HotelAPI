import django.utils.timezone

from django.db import models


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


class BoockedRoom(models.Model):
    username = models.CharField(max_length=30)
    bookedRoomId = models.ForeignKey(Room, on_delete=models.CASCADE)
    bookedDateFrom = models.DateField('с:', default=django.utils.timezone.now())
    bookedDateTo = models.DateField('по:', default=django.utils.timezone.now())
    class Meta:
        verbose_name = 'Забронированная комната'
        verbose_name_plural = 'Забронированные комнаты'


    def __str__(self):
        room = Room.objects.get(number=self.bookedRoomId)
        print(room)
        return f'Комната №{room.number} забронирована пользователем {self.username}'
