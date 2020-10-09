from django.contrib.auth import get_user_model
from django.db.models import Model, CharField, FloatField, DateTimeField, ForeignKey, CASCADE, SET_NULL
from gameservice.exceptions import PlayerNotFoundException, ActionNotFoundException
from model_utils import Choices
from model_utils.fields import StatusField
from model_utils.managers import InheritanceManager
from picklefield.fields import PickledObjectField

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

    req_num_players = None
    game_type = None

    """Django Templates"""

    @property
    def template_path(self):
        return f"gamemaster/{self._meta.model_name}_detail.html"

    @property
    def stylesheet_path(self):
        return f"gamemaster/stylesheets/{self._meta.model_name[:-4]}.css"

    @property
    def javascript_module_path(self):
        return f"gamemaster/javascripts/{self._meta.model_name[:-4]}.mjs"

    @property
    def model_name(self):
        return self._meta.object_name

    """Game Creation"""

    @property
    def player_labels(self):
        labels = [seat.user.username for seat in self.seats.all() if seat.status == Seat.STATUS.ONLINE]

        if self.game is not None:
            for label in list(map(lambda player: player.label, self.game.players))[1:]:
                if label in labels:
                    labels = labels[labels.index(label):] + labels[:labels.index(label)]
                    break

        return labels

    @property
    def game_config(self):
        return {
            "labels": self.player_labels
        }

    def create_game(self):
        game_config = self.game_config

        if len(game_config["labels"]) < self.req_num_players:
            raise GameCreationException

        return self.game_type(**game_config)

    """Game Service Properties"""

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

    """Constant Member Variables/Methods"""

    @property
    def users(self):
        return list(seat.user for seat in self.seats.all() if seat.user is not None)

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

    def seat(self, user):
        if isinstance(user, str):
            user = get_user_model().objects.get(username=user)

        if user in self.users:
            return self.seats.get(user=user)
        else:
            return None

    def stats(self, career):
        return []

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
            seat.status = Seat.STATUS.ONLINE
            seat.save()
            self.save()
        except (AssertionError, PlayerNotFoundException, ActionNotFoundException):
            raise GameActionException

    def command(self, user, command):
        try:
            assert Seat.STATUS.valid(command) and user.is_authenticated

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
            assert ((any(seat.status == Seat.STATUS.OFFLINE for seat in self.seats.all()) or
                     sum(seat.status == Seat.STATUS.ONLINE for seat in self.seats.all()) >= self.req_num_players) and
                    self.game is None) or (self.game is not None and self.game.terminal)

            for seat in self.seats.all():
                if seat.status == Seat.STATUS.OFFLINE:
                    seat.kick()

            if self.game is not None:
                for player in self.game.players:
                    for stat in self.stats(get_user_model().objects.get(username=player.label).career):
                        stat.update(player.payoff)

            try:
                self.game = self.create_game()
            except GameCreationException:
                self.game = None

            self.save()
        except AssertionError:
            raise GameActionException


class Seat(Model):
    class STATUS:
        ONLINE = "Online"
        AWAY = "Away"
        OFFLINE = "Offline"

        @classmethod
        def valid(cls, status):
            return status == cls.ONLINE or status == cls.AWAY or status == cls.OFFLINE

    status_list = Choices(STATUS.ONLINE, STATUS.AWAY, STATUS.OFFLINE)

    room = ForeignKey(Room, on_delete=CASCADE, related_name="seats")

    user = ForeignKey(get_user_model(), on_delete=SET_NULL, related_name="seats", blank=True, null=True)
    status = StatusField(choices_name="status_list", default=None, blank=True, null=True)

    @property
    def description(self):
        return None if self.user is None else "\n".join(map(str, self.room.stats(self.user.career)))

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
