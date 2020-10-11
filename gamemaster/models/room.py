from django.contrib.auth import get_user_model
from django.db.models import Model, CharField, FloatField, DateTimeField, ForeignKey, BooleanField, CASCADE, SET_NULL
from gameservice.exceptions import PlayerNotFoundException, ActionNotFoundException
from model_utils.managers import InheritanceManager
from picklefield.fields import PickledObjectField

from ..exceptions import GameCreationException, GameActionException


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

    @property
    def timeout(self):
        if self.game is None and (any(seat.user is not None and not seat.status for seat in self.seats.all()) or
                                  sum(seat.status for seat in self.seats.all()) >= self.req_num_players):
            return 0
        elif self.game is not None and self.game.terminal:
            return self.restart_timeout
        else:
            return None

    @property
    def config(self):
        return {
            "description": self.description,
            "num_seats": self.num_seats,
            "req_num_players": self.req_num_players,
        }

    """Game Service Properties"""

    @property
    def context(self):
        if self.game is not None:
            return self.game.context.info
        else:
            return None

    def actions(self, user):
        try:
            assert self.game is not None

            return list(self.game.players[user.username].actions)
        except (AssertionError, PlayerNotFoundException):
            return []

    """Django Templates"""

    @property
    def template_path(self):
        return f"gamemaster/{self._meta.model_name[:-4]}.html"

    @property
    def stylesheet_paths(self):
        return ["gamemaster/stylesheets/room.css"]

    @property
    def javascript_paths(self):
        return ["gamemaster/javascripts/room.js"]

    @property
    def model_name(self):
        return self._meta.object_name

    """Game Creation"""

    @property
    def player_labels(self):
        labels = [seat.user.username for seat in self.seats.all() if seat.status]

        if self.game is not None:
            for label in [player.label for player in self.game.players][1:]:
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

    """Constant Member Variables/Methods"""

    @property
    def users(self):
        return list(seat.user for seat in self.seats.all() if seat.user is not None)

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
            seat.status = True
            seat.save()
            self.save()
        except (AssertionError, PlayerNotFoundException, ActionNotFoundException):
            raise GameActionException

    def toggle(self, user):
        try:
            seat = self.seat(user)

            if seat is None:
                seat = next(seat for seat in self.seats.all() if seat.user is None)
                seat.user = user

            seat.status = not seat.status
            seat.save()
            self.save()
        except StopIteration:
            raise GameActionException

    def autoplay(self):
        try:
            assert self.game is None or self.game.terminal

            for seat in self.seats.all():
                if seat.user is not None and not seat.status:
                    seat.clear()

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
    room = ForeignKey(Room, on_delete=CASCADE, related_name="seats")

    user = ForeignKey(get_user_model(), on_delete=SET_NULL, related_name="seats", blank=True, null=True)
    status = BooleanField(default=False)

    updated_on = DateTimeField(auto_now=True)

    @property
    def stats(self):
        return None if self.user is None else list(map(str, self.room.stats(self.user.career)))

    def clear(self):
        self.user = None
        self.status = False
        self.save()

    def player(self, user):
        try:
            assert self.room.game is not None and self.user is not None

            return self.room.game.players[self.user.username].private_info if self.user == user else \
                self.room.game.players[self.user.username].public_info
        except (AssertionError, PlayerNotFoundException):
            return None
