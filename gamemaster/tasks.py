from datetime import timedelta
from threading import Thread

from django.db.utils import OperationalError
from django.utils import timezone

from .exceptions import GameActionException
from .models import Room


def monitor_rooms():
    while True:
        try:
            for room in Room.objects.select_subclasses():
                try:
                    if room.updated_on + timedelta(seconds=room.timeout) <= timezone.now():
                        room.autoplay()
                except (TypeError, GameActionException):
                    pass
        except OperationalError:
            pass


def monitor():
    Thread(target=monitor_rooms, daemon=True).start()
