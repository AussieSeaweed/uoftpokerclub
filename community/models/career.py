from annoying.fields import AutoOneToOneField
from django.contrib.auth import get_user_model
from django.db.models import Model, CASCADE, BigIntegerField


class Career(Model):
    user = AutoOneToOneField(get_user_model(), unique=True, on_delete=CASCADE)

    def __str__(self):
        return self.user.username


class Stat(Model):
    career = AutoOneToOneField(Career, unique=True, on_delete=CASCADE)

    payoffs = BigIntegerField(default=0)
    wins = BigIntegerField(default=0)
    losses = BigIntegerField(default=0)
    ties = BigIntegerField(default=0)
    num_plays = BigIntegerField(default=0)

    @property
    def payoff_rate(self):
        return self.payoffs / self.num_plays if self.num_plays else 0

    def update(self, payoff):
        self.payoffs += payoff

        if payoff > 0:
            self.wins += payoff
        elif payoff < 0:
            self.losses -= payoff
        else:
            self.ties += 1

        self.num_plays += 1
        self.save()

    def __str__(self):
        return f"Profit: {self.payoffs} ({round(self.payoff_rate, 2)}/h)"

    class Meta:
        abstract = True


class PokerStat(Stat):
    class Meta:
        abstract = True


class NLHEStat(PokerStat):
    pass
