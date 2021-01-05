from __future__ import annotations

from django.contrib.auth import get_user_model
from django.db import models
from gameframe.game import Game, Actor
from model_utils.managers import InheritanceManager
from picklefield.fields import PickledObjectField
from datetime import datetime
from collections.abc import Mapping
from typing import Any, Generic, Optional, TypeVar
from django.contrib.auth.models import User

__all__ = ['Room', 'Seat']

G = TypeVar('G', bound=Game)


class Room(models.Model, Generic[G]):
    objects: InheritanceManager = InheritanceManager()

    name: str = models.CharField(max_length=255, unique=True)
    timeout: float = models.FloatField()
    updated_on: datetime = models.DateTimeField(auto_now=True)

    game: G = PickledObjectField(blank=True, null=True)

    def __str__(self) -> str:
        return self.name

    def information_set(self, user: User) -> Mapping[str, Any]:
        information_set: dict[str, Any] = {'seats': list(map(lambda seat: seat.information, self.seats))}

        if self.game is not None:
            if self.seat(user) is not None and self.seat(user).index is not None:
                player: Actor = self.game.players[self.seat(user).index]
            else:
                player: Actor = self.game.nature

            information_set['information_set'] = player.information_set

        return information_set

    def seat(self, user: User) -> Optional[Seat]:
        for seat in self.seats:
            if seat.user == user:
                return seat
        else:
            return None

    def update(self, user: User) -> None:
        pass

    def create_game(self) -> G:
        pass


class Seat(models.Model):
    room: Room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='seats')
    user: User = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, related_name='seats', blank=True, null=True)

    index: int = models.IntegerField(blank=True, null=True)

    @property
    def information(self) -> Mapping[str, Any]:
        return {
            'username': self.user.username,
            'index': self.index,
        }
