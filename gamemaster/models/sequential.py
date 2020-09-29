from abc import abstractmethod

from django.db.models import FloatField

from .room import Room


class SequentialRoom(Room):
    user_timeout = FloatField(default=30)
    nature_timeout = FloatField(default=1)

    @abstractmethod
    def skip(self):
        pass
