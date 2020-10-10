from django.apps import AppConfig


class GamemasterConfig(AppConfig):
    name = 'gamemaster'

    def ready(self):
        from .signals import update_rooms

        update_rooms()
