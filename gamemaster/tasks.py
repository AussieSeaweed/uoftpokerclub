from datetime import timedelta
from threading import Thread

from django.db.utils import OperationalError
from django.utils import timezone

from .exceptions import GameActionException
from .models import Room, Seat


def monitor_rooms():
    while True:
        try:
            for room in Room.objects.select_subclasses():
                try:
                    for seat in room.seats.all():
                        if seat.status == Seat.STATUS.AWAY and \
                                seat.updated_on + timedelta(seconds=room.idle_timeout) <= timezone.now():
                            seat.status = Seat.STATUS.OFFLINE
                            seat.save()

                    if room.updated_on + timedelta(seconds=room.timeout) <= timezone.now():
                        room.autoplay()
                except (TypeError, GameActionException):
                    pass
        except OperationalError:
            pass


def monitor():
    Thread(target=monitor_rooms, daemon=True).start()
