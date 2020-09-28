from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

from .exceptions import GameCreationException
from .models import Room, Seat


def update_model(sender, instance, created, **kwargs):
    if issubclass(sender, Room) and created:
        attach_seats(instance)

    if issubclass(sender, Room) or sender is Seat:
        update_room(instance if issubclass(sender, Room) else instance.room)


def attach_seats(room):
    for i in range(room.num_seats):
        Seat.objects.create(room=room)


def update_room(room):
    if room.game is None:
        try:
            room.create_game()
        except GameCreationException:
            pass

    async_to_sync(get_channel_layer().group_send)(repr(room), {"type": "send_infoset"})
