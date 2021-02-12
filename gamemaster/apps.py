from django.apps import AppConfig


class GamemasterConfig(AppConfig):
    name = 'gamemaster'

    def ready(self):
        from gamemaster.signals import setup

        setup()
