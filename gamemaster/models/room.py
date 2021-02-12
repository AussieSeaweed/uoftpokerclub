from django.contrib.auth import get_user_model
from django.db import models
from model_utils.managers import InheritanceManager
from picklefield.fields import PickledObjectField
from itertools import count

from gamemaster.exceptions import GameCreationException, NoEmptySeatException, SeatNotFoundException


class Seat:
    def __init__(self):
        self.index = None
        self.__user_id = None

    @property
    def user(self):
        return None if self.__user_id is None else get_user_model().objects.get(self.__user_id)

    @user.setter
    def user(self, user):
        self.__user_id = None if user is None else user.id

    @property
    def information(self):
        return {
            'index': self.index,
            'user': None if self.user is None else {
                'username': self.user.username,
            },
        }


class Room(models.Model):
    objects = InheritanceManager()

    name = models.CharField(max_length=255, unique=True)
    timeout = models.FloatField(default=1)
    updated_on = models.DateTimeField(auto_now=True)

    game = PickledObjectField(blank=True, null=True)
    seats = PickledObjectField(blank=True, null=True)

    def __repr__(self):
        return f'room-{self.pk}'

    @property
    def user_count(self):
        return sum(seat.user is not None for seat in self.seats)

    @property
    def empty_seat(self):
        try:
            return next(seat.user is None for seat in self.seats)
        except StopIteration:
            raise NoEmptySeatException

    @property
    def seat_count(self):
        raise NotImplemented

    @property
    def game_name(self):
        raise NotImplemented

    def seat(self, user):
        for seat in self.seats:
            if seat.user == user:
                return seat

        raise SeatNotFoundException

    def update(self):
        updated = False

        if self.seats is None:
            self.seats = [Seat() for _ in range(self.seat_count)]

            updated = True

        if self.game is not None and self.game.terminal:
            self.game = None

            for seat in self.seats:
                seat.index = None

            updated = True

        if self.game is None:
            try:
                self.game = self.create_game()

                for seat, index in zip(filter(lambda seat: seat.user is not None, self.seats), count()):
                    seat.index = index

                updated = True
            except GameCreationException:
                pass

        return updated

    def create_game(self):
        raise NotImplemented

    class Meta:
        verbose_name = 'Room'
