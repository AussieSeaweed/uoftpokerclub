from abc import abstractmethod

from django.contrib.auth import get_user_model
from django.db import models
from gameservice.exceptions import PlayerNotFoundException, ActionNotFoundException
from model_utils.managers import InheritanceManager
from picklefield.fields import PickledObjectField

from ..exceptions import GameActionException


class Room(models.Model):
    name = models.CharField(max_length=255, unique=True)
    game = PickledObjectField(blank=True, null=True)

    objects = InheritanceManager()

    """Room Variables"""

    description = None
    num_seats = None

    @property
    def stylesheet_path(self):
        return f"gamemaster/stylesheets/{self._meta.model_name}.css"

    @property
    def javascript_module_path(self):
        return f"gamemaster/javascripts/{self._meta.model_name}.mjs"

    @property
    def model_name(self):
        return self._meta.object_name

    @property
    def status(self):
        return f"{len(self.users)}/{self.num_seats} Online"

    @property
    def users(self):
        return list(seat.user for seat in self.seats.all() if seat.user is not None)

    @property
    def context(self):
        return None if self.game is None else self.game.context.info

    def actions(self, user):
        try:
            return list(self.game.players[user.username].actions)
        except PlayerNotFoundException:
            raise GameActionException

    def act(self, user, action):
        try:
            self.game.players[user.username].actions[action].act()
            self.save()
        except (PlayerNotFoundException, ActionNotFoundException):
            raise GameActionException

    @abstractmethod
    def create_game(self):
        pass

    def __str__(self):
        return self.name

    def __repr__(self):
        return f"room_{self.id}"


class Seat(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name="seats")
    user = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, related_name="seats", blank=True, null=True)

    def player(self, user):
        if self.room.game is None or self.user is None:
            return None
        else:
            try:
                return self.room.game.players[self.user.username].private_info if self.user == user else \
                    self.room.game.players[self.user.username].public_info
            except PlayerNotFoundException:
                return None
