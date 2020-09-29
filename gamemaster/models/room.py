from abc import abstractmethod

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.contrib.auth import get_user_model
from django.db.models import Model, CharField, DateTimeField, ForeignKey, CASCADE, SET_NULL
from django.db.models.signals import post_save
from django.dispatch import receiver
from gameservice.exceptions import PlayerNotFoundException, ActionNotFoundException
from model_utils import Choices
from model_utils.fields import StatusField
from model_utils.managers import InheritanceManager
from picklefield.fields import PickledObjectField

from ..exceptions import GameCreationException, GameActionException, RoomCommandException


class Room(Model):
    name = CharField(max_length=255, unique=True)
    game = PickledObjectField(blank=True, null=True)

    updated_on = DateTimeField(auto_now=True)

    objects = InheritanceManager()

    """Room Variables"""

    description = None
    num_seats = None

    """Constant Methods"""

    @property
    def stylesheet_path(self):
        return f"gamemaster/stylesheets/{self._meta.model_name[:-4]}.css"

    @property
    def javascript_module_path(self):
        return f"gamemaster/javascripts/{self._meta.model_name[:-4]}.mjs"

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
        try:
            assert self.game is not None
            return self.game.context.info
        except AssertionError:
            return None

    def actions(self, user):
        try:
            assert self.game is not None
            return list(self.game.players[user.username].actions)
        except (AssertionError, PlayerNotFoundException):
            return []

    def __str__(self):
        return self.name

    def __repr__(self):
        return f"room_{self.id}"

    """Non-Constant Methods"""

    def _seat(self, user):
        if user in self.users:
            return self.seats.get(user=user)
        elif len(self.users) != self.num_seats:
            seat = next(seat for seat in self.seats.all() if seat.user is None)

            seat.user = user
            seat.save()

            return seat
        else:
            return None

    def act(self, user, action):
        try:
            assert self.game is not None and user in self.users

            self.game.players[user.username].actions[action].act()

            seat = self._seat(user)
            seat.status = "Online"

            seat.save()
            self.save()
        except (AssertionError, PlayerNotFoundException, ActionNotFoundException):
            raise GameActionException

    def command(self, user, command):
        try:
            seat = self._seat(user)
            assert seat is not None and command in Seat.STATUS and command is not None

            seat.status = command

            seat.save()
            self.save()
        except AssertionError:
            raise RoomCommandException

    @abstractmethod
    def create_game(self):
        pass

    def destroy_game(self):
        for seat in self.seats.all():
            if seat.status == "Offline":
                seat.kick()

        self.game = None
        self.save()


class Seat(Model):
    STATUS = Choices("Online", "Away", "Offline")

    room = ForeignKey(Room, on_delete=CASCADE, related_name="seats")
    user = ForeignKey(get_user_model(), on_delete=SET_NULL, related_name="seats", blank=True, null=True)
    status = StatusField(default=None, blank=True, null=True)

    def kick(self):
        self.user = None
        self.status = None
        self.save()

    def player(self, user):
        try:
            assert self.room.game is not None and self.user is not None

            return self.room.game.players[self.user.username].private_info if self.user == user else \
                self.room.game.players[self.user.username].public_info
        except (AssertionError, PlayerNotFoundException):
            return None


@receiver(post_save)
def update_room(sender, instance, created, **kwargs):
    if issubclass(sender, Room):
        if created:
            for i in range(instance.num_seats):
                Seat.objects.create(room=instance)

        if instance.game is None:
            try:
                instance.create_game()
            except GameCreationException:
                pass

        if instance.game is not None and instance.game.terminal:
            instance.destroy_game()

        async_to_sync(get_channel_layer().group_send)(repr(instance), {"type": "send_infoset"})
