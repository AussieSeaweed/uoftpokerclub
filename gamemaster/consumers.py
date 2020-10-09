from asgiref.sync import async_to_sync
from channels.generic.websocket import JsonWebsocketConsumer

from .exceptions import GameActionException, RoomCommandException
from .models import Room, Seat
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

        if self.user in self.room.users:
            self.room.command(self.user, Seat.STATUS.ONLINE)

        self.accept()
        self.send_infoset()

    def disconnect(self, code):
        async_to_sync(self.channel_layer.group_discard)(repr(self.room), self.channel_name)

        if self.user in self.room.users:
            self.room.command(self.user, Seat.STATUS.OFFLINE)

    def receive_json(self, content, **kwargs):
        try:
            if isinstance(content, str) and content[:1] == "/":
                self.room.command(self.user, content[1:])
            else:
                self.room.act(self.user, content)
        except (GameActionException, RoomCommandException):
            pass

    def send_infoset(self, event=None):
        self.send_json(RoomSerializer(instance=self.room, context={"user": self.user}).data)
