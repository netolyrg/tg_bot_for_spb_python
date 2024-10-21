from django.db import models


class Profile(models.Model):
    tg_id = models.PositiveIntegerField()


class EventType(models.Model):
    name = models.CharField(max_length=64, blank=False)
    description = models.TextField(default='', blank=True)


class Slot(models.Model):
    class Status(models.TextChoices):
        FREE = 'free', 'Free'
        RESERVED = 'reserved', 'Reserved'

    status = models.CharField(
        max_length=10, choices=Status.choices, default=Status.FREE
    )
    type_of_event = models.ForeignKey(
        to=EventType, on_delete=models.SET_NULL, related_name='slots', null=True
    )
    time_of_event = models.DateTimeField()
    reserved_by = models.ForeignKey(
        to=Profile, on_delete=models.SET_NULL, related_name='slots', null=True, blank=True
    )


