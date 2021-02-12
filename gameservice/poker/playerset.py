from gameservice.game.playersets import PlayerSet


class PokerPlayerSet(PlayerSet):
    @property
    def bets(self):
        return [player.bet for player in self]

    def next_relevant(self, player):
        if not self.num_relevant:
            return self.nature

        player = self.next(player)

        while not player.relevant and player is not self.game.context.aggressor:
            player = self.next(player)

        return self.nature if player is self.game.context.aggressor else player

    @property
    def num_relevant(self):
        return sum(player.relevant for player in self)

    @property
    def num_mucked(self):
        return sum(player.mucked for player in self)
