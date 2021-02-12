from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.db.models.signals import post_save
from django.dispatch import receiver

from gamemaster.models import Room


@receiver(post_save)
def update_room(instance, **kwargs):
    if isinstance(instance, Room):
        if instance.update():
            instance.save()
        else:
            async_to_sync(get_channel_layer().group_send)(repr(instance), {'type': 'send_information_set'})


def setup() -> None:
    pass
