from django.db.models import FloatField

from .room import Room
from ..exceptions import GameActionException


class SequentialRoom(Room):
    player_timeout = FloatField(default=30)
    nature_timeout = FloatField(default=1)

    """Constant Methods/Properties"""

    @property
    def timeout(self):
        try:
            assert super().timeout is None and self.game is not None and self.game.player is not None
            return self.nature_timeout if self.game.player.nature else self.player_timeout
        except AssertionError:
            return super().timeout

    """Non-Constant Methods"""

    def autoplay(self):
        try:
            try:
                super().autoplay()
            except GameActionException:
                assert self.game is not None and self.game.player is not None
                self.game.player.actions[next(iter(self.game.player.actions))].act()

                self.save()
        except (AssertionError, StopIteration):
            raise GameActionException
