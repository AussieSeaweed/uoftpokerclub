from django.apps import AppConfig
from django.db.models.signals import post_save


class GamemasterConfig(AppConfig):
    name = 'gamemaster'

    def ready(self):
        from .signals import update_room
        from .tasks import monitor

        post_save.connect(update_room)
        monitor()
