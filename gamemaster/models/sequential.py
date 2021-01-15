from random import choice

from gamemaster.models.room import Room


class SequentialRoom(Room):
    def update(self):
        updated = super().update()

        if self.game.actor.nature:
            choice(self.game.actor.actions).act()
            updated = True

        return updated

    class Meta:
        verbose_name = 'Sequential Room'
