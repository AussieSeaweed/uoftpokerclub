from datetime import timedelta
from threading import Timer

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.db.models.signals import post_save
from django.db.utils import OperationalError
from django.dispatch import receiver
from django.utils.timezone import now

from .models import Room, Seat

room_timers = {}


class RoomTimer(Timer):
    def __init__(self, room):
        super().__init__((room.updated_on + timedelta(seconds=room.timeout) - now()).total_seconds(), self.autoplay)

        self.created_on = room.updated_on
        self.room_pk = room.pk

        self.setDaemon(True)
        self.start()

    @property
    def room(self):
        return Room.objects.get_subclass(pk=self.room_pk)

    def autoplay(self):
        if self.created_on == self.room.updated_on:
            self.room.autoplay()


@receiver(post_save)
def update_room(sender, instance, created, **kwargs):
    if issubclass(sender, Room):
        if created:
            for i in range(instance.num_seats):
                Seat.objects.create(room=instance)

        async_to_sync(get_channel_layer().group_send)(repr(instance), {"type": "send_infoset"})

        if instance.timeout is not None:
            if instance in room_timers:
                room_timers[instance].cancel()

            room_timers[instance] = RoomTimer(instance)


def update_rooms():
    try:
        for room in Room.objects.select_subclasses():
            room.save()
    except OperationalError:
        pass
