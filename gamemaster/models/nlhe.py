from gameservice.nlhe.game import NLHEGame

from .poker import PokerRoom


class NLHERoom(PokerRoom):
    game_type = NLHEGame
    poker_description = "No-Limit Texas Hold'em"
    num_hole_cards = 2
    num_board_cards = 5

    def stats(self, career):
        return super().stats(career) + [career.nlhestat]

    class Meta:
        verbose_name = "No-Limit Texas Hold'em Room"
