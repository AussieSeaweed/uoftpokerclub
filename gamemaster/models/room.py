from __future__ import annotations

from abc import ABC, abstractmethod
from collections import defaultdict
from collections.abc import Mapping, MutableSequence, Sequence
from datetime import datetime
from typing import Any, Generic, Optional, TypeVar

from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.db import models
from gameframe.game import Actor, Game
from picklefield.fields import PickledObjectField

from gamemaster.exceptions import GameCreationException, NoEmptySeatException, SeatNotFoundException

__all__: Sequence[str] = ['Seat', 'Room']

G = TypeVar('G', bound=Game)


class Seat:
    def __init__(self):
        self.__index: Optional[int] = None
        self.__user_id: Optional[int] = None

    @property
    def index(self) -> Optional[int]:
        return self.__index

    @index.setter
    def index(self, index: Optional[int]) -> None:
        self.__index = index

    @property
    def user(self) -> Optional[User]:
        return None if self.__user_id is None else get_user_model().objects.get(self.__user_id)

    @user.setter
    def user(self, user: Optional[User]) -> None:
        self.__user_id = None if user is None else user.id

    @property
    def information(self) -> Mapping[str, Any]:
        return {
            'index': self.index,
            'user': None if self.user is None else {
                'username': self.user.username,
            },
        }


class Room(models.Model, Generic[G], ABC):
    name: str = models.CharField(max_length=255, unique=True)
    timeout: float = models.FloatField()
    updated_on: datetime = models.DateTimeField(auto_now=True)

    game: Optional[G] = PickledObjectField(blank=True, null=True)
    seats: MutableSequence[Seat] = PickledObjectField(default=lambda: defaultdict(Seat))

    seat_count: int

    def __str__(self) -> str:
        return self.name

    @property
    def user_count(self) -> int:
        count: int = 0

        for i in range(self.seat_count):
            if self.seats[i].user is not None:
                count += 1

        return count

    @property
    def empty_seat(self) -> Seat:
        for i in range(self.seat_count):
            if self.seats[i].user is None:
                return self.seats[i]

        raise NoEmptySeatException

    def seat(self, user: User) -> Seat:
        for i in range(self.seat_count):
            if self.seats[i].user == user:
                return self.seats[i]

        raise SeatNotFoundException

    def data(self, user: User) -> Mapping[str, Any]:
        data: dict[str, Any] = {'seats': [self.seats[i].information for i in range(self.seat_count)]}

        if self.game is not None:
            index: Optional[int]

            try:
                index = self.seat(user).index
            except SeatNotFoundException:
                index = None

            player: Actor = self.game.nature if index is None else self.game.players[self.seat(user).index]

            data['information_set'] = player.information_set
        else:
            data['information_set'] = None

        return data

    def update(self) -> bool:
        updated: bool = False

        if self.game is not None and self.game.terminal:
            self.game = None

            for i in range(self.seat_count):
                self.seats[i].user = None
                self.seats[i].index = None

            updated = True

        if self.game is None:
            try:
                self.game = self.create_game()

                count: int = 0

                for i in range(self.seat_count):
                    if self.seats[i].user is not None:
                        self.seats[i].index = None
                        count += 1

                updated = True
            except GameCreationException:
                pass

        return updated

    @abstractmethod
    def create_game(self) -> G:
        pass

    class Meta:
        abstract: bool = True
        verbose_name: str = 'Room'
