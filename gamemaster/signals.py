from typing import Any

from django.db.models.signals import post_save
from django.dispatch import receiver

from gamemaster.models import Room


@receiver(post_save)
def update_room(instance: Any, **kwargs) -> None:
    if isinstance(instance, Room) and instance.update():
        pass  # TODO: SEND INFORMATION
