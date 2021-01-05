from abc import ABC

from typing import TypeVar
from collections.abc import Sequence
from gameframe.sequential import SequentialGame
from random import choice

from gamemaster.models.room import Room

__all__: Sequence[str] = ['SequentialRoom']

SG = TypeVar('SG', bound=SequentialGame)


class SequentialRoom(Room[SG], ABC):
    def update(self) -> bool:
        updated: bool = super().update()

        if self.game.actor.nature:
            choice(self.game.actor.actions).act()
            updated = True

        return updated

    class Meta:
        abstract: bool = True
        verbose_name: str = 'Sequential Room'
