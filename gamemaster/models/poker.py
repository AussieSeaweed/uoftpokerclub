from django.db.models import PositiveIntegerField, IntegerChoices
from gameservice.exceptions import PlayerNotFoundException

from .sequential import SequentialRoom


class PokerRoom(SequentialRoom):
    class SeatConfig(IntegerChoices):
        SIX_MAX = 6
        NINE_MAX = 9

    num_seats = PositiveIntegerField(choices=SeatConfig.choices)

    ante = PositiveIntegerField(default=0)
    small_blind = PositiveIntegerField(default=1)
    big_blind = PositiveIntegerField(default=2)
    starting_stack = PositiveIntegerField(default=200)

    """Room Variables"""

    poker_description = None

    @property
    def description(self):
        return f"{self.num_seats}-Max {self.poker_description} ({self.starting_stack // self.big_blind} bb)"

    req_num_players = 2

    num_hole_cards = 0
    num_board_cards = 0

    @property
    def config(self):
        return {
            **super().config,
            "num_hole_cards": self.num_hole_cards,
            "num_board_cards": self.num_board_cards,
        }

    """Django Templates"""

    @property
    def template_path(self):
        return f"gamemaster/poker{self.num_seats}room_detail.html"

    @property
    def stylesheet_path(self):
        return f"gamemaster/stylesheets/poker.css"

    @property
    def javascript_module_path(self):
        return f"gamemaster/javascripts/poker.mjs"

    @property
    def model_name(self):
        return f"PokerRoom"

    """Constant methods/Properties"""

    @property
    def game_config(self):
        game_config = super().game_config

        starting_stacks = []

        for label in game_config["labels"]:
            try:
                assert self.game is not None

                starting_stacks.append(max(self.game.players[label].stack, self.starting_stack))
            except (AssertionError, PlayerNotFoundException):
                starting_stacks.append(self.starting_stack)

        game_config.update({
            "ante": self.ante,
            "blinds": [self.small_blind, self.big_blind],
            "starting_stacks": starting_stacks,
        })

        return game_config
