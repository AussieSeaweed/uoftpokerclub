from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

from .models import Room, Seat


def update_room(sender, instance, created, **kwargs):
    if issubclass(sender, Room):
        if created:
            for i in range(instance.num_seats):
                Seat.objects.create(room=instance)

        async_to_sync(get_channel_layer().group_send)(repr(instance), {"type": "send_infoset"})
