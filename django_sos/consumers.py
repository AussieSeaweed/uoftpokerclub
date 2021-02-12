from django.apps import apps
from channels.generic.websocket import AsyncJsonWebsocketConsumer

from django_sos.live import live_consumers


class LiveConsumer(AsyncJsonWebsocketConsumer):
    @property
    def instance(self):
        return apps.get_model(
            self.scope['url_route']['kwargs']['app_label'],
            self.scope['url_route']['kwargs']['model_name'],
        ).objects.get(pk=self.scope['url_route']['kwargs']['pk'])

    def connect(self):
        self.accept()

        live_consumers(self.instance).add(self)

    def disconnect(self, code):
        live_consumers(self.instance).remove(self)

    def send_model_live(self):
