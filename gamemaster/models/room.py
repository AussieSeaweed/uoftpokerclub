from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.contrib.auth import get_user_model
from django.db.models import Model, CharField, FloatField, DateTimeField, ForeignKey, CASCADE, SET_NULL
from django.db.models.signals import post_save
from django.dispatch import receiver
from gameservice.exceptions import PlayerNotFoundException, ActionNotFoundException
from model_utils import Choices
from model_utils.fields import StatusField
from model_utils.managers import InheritanceManager
from picklefield.fields import PickledObjectField
from datetime import timedelta, datetime

from ..exceptions import GameCreationException, GameActionException, RoomCommandException


class Room(Model):
    name = CharField(max_length=255, unique=True)
    game = PickledObjectField(blank=True, null=True)
    restart_timeout = FloatField(default=5)

    updated_on = DateTimeField(auto_now=True)

    objects = InheritanceManager()

    """Room Variables"""

    description = None
    num_seats = None

    """Constant Methods/Properties"""

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

    @property
    def config(self):
        return {
            "updated_on": str(self.updated_on),
            "timeout": self.timeout,
        }

    @property
    def timeout(self):
        try:
            assert self.game is not None
            return self.restart_timeout if self.game.terminal else None
        except AssertionError:
            return 0

    def actions(self, user):
        try:
            assert self.game is not None
            return list(self.game.players[user.username].actions)
        except (AssertionError, PlayerNotFoundException):
            return []

    def seat(self, user):
        if isinstance(user, str):
            user = get_user_model().objects.get(username=user)

        if user in self.users:
            return self.seats.get(user=user)
        else:
            return None

    def create_game(self):
        raise GameCreationException

    def __str__(self):
        return self.name

    def __repr__(self):
        return f"room_{self.id}"

    """Non-Constant Methods"""

    def act(self, user, action):
        try:
            assert self.game is not None and user in self.users
            self.game.players[user.username].actions[action].act()

            seat = self.seat(user)
            seat.status = "Online"
            seat.save()
            self.save()
        except (AssertionError, PlayerNotFoundException, ActionNotFoundException):
            raise GameActionException

    def command(self, user, command):
        try:
            assert command in Seat.STATUS
            seat = self.seat(user)

            if seat is None:
                seat = next(seat for seat in self.seats.all() if seat.user is None)
                seat.user = user

            seat.status = command
            seat.save()
            self.save()
        except (AssertionError, StopIteration):
            raise RoomCommandException

    def autoplay(self):
        try:
            assert self.game is None or self.game.terminal

            for seat in self.seats.all():
                if seat.status == "Offline":
                    seat.kick()

            try:
                self.game = self.create_game() if self.game is None else None
            except GameCreationException:
                pass

            self.save()
        except AssertionError:
            raise GameActionException


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

        async_to_sync(get_channel_layer().group_send)(repr(instance), {"type": "send_infoset"})


def monitor_rooms():
    for room in Room.objects.select_subclasses():
        if room.timeout is not None and (room.updated_on + timedelta(seconds=room.timeout)) < datetime.now():
            try:
                room.autoplay()
            except GameActionException:
                pass
