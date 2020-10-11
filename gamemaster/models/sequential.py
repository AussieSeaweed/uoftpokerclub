from django.db.models import FloatField

from .room import Room
from ..exceptions import GameActionException


class SequentialRoom(Room):
    player_timeout = FloatField(default=30)
    nature_timeout = FloatField(default=1)

    """Django Templates"""

    @property
    def stylesheet_paths(self):
        return [
            *super().stylesheet_paths,
            "gamemaster/stylesheets/sequential.css",
        ]

    @property
    def javascript_paths(self):
        return [
            *super().javascript_paths,
            "gamemaster/javascripts/sequential.js",
        ]

    """Room Variables"""

    @property
    def timeout(self):
        try:
            assert super().timeout is None and self.game is not None and self.game.player is not None

            if self.game.player.nature:
                return self.nature_timeout
            else:
                return self.player_timeout if self.seat(self.game.player.label).status else 0
        except AssertionError:
            return super().timeout

    """Non-Constant Methods"""

    def autoplay(self):
        try:
            super().autoplay()
        except GameActionException:
            try:
                assert self.game is not None and self.game.player is not None

                player = self.game.player
                player.actions[next(iter(player.actions))].act()

                if not player.nature:
                    seat = self.seat(player.label)
                    seat.status = False
                    seat.save()

                self.save()
            except (AssertionError, StopIteration):
                raise GameActionException
