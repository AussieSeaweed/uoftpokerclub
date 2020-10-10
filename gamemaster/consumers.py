from asgiref.sync import async_to_sync
from channels.generic.websocket import JsonWebsocketConsumer

from .exceptions import GameActionException
from .models import Room
from .serializers import RoomSerializer


class RoomConsumer(JsonWebsocketConsumer):
    @property
    def user(self):
        return self.scope["user"]

    @property
    def room(self):
        return Room.objects.get_subclass(pk=self.scope["url_route"]["kwargs"]["pk"])

    def connect(self):
        async_to_sync(self.channel_layer.group_add)(repr(self.room), self.channel_name)

        if self.user in self.room.users and not self.room.seat(self.user).status:
            self.room.toggle(self.user)

        self.accept()
        self.send_infoset()

    def disconnect(self, code):
        async_to_sync(self.channel_layer.group_discard)(repr(self.room), self.channel_name)

        if self.user in self.room.users and self.room.seat(self.user).status:
            self.room.toggle(self.user)

    def receive_json(self, content, **kwargs):
        try:
            if content is None:
                self.room.toggle(self.user)
            else:
                self.room.act(self.user, content)
        except GameActionException:
            pass

    def send_infoset(self, event=None):
        self.send_json(RoomSerializer(instance=self.room, context={"user": self.user}).data)
