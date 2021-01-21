from asgiref.sync import async_to_sync
from channels.generic.websocket import JsonWebsocketConsumer

from gamemaster.models import Room
from gamemaster.serializers import RoomSerializer


class RoomConsumer(JsonWebsocketConsumer):
    @property
    def user(self):
        return self.scope['user']

    @property
    def room(self):
        return Room.objects.get_subclass(pk=self.scope['url_route']['kwargs']['pk'])

    def connect(self):
        async_to_sync(self.channel_layer.group_add)(repr(self.room), self.channel_name)
        #
        # if self.user in self.room.users and not self.room.seat(self.user).status:
        #     self.room.toggle(self.user)

        self.accept()
        self.send_information_set()

    def disconnect(self, code):
        async_to_sync(self.channel_layer.group_discard)(repr(self.room), self.channel_name)
        #
        # if self.user in self.room.users and self.room.seat(self.user).status:
        #     self.room.toggle(self.user)

    def receive_json(self, content, **kwargs):
        raise NotImplemented
        # try:
        #     if content is None:
        #         self.room.toggle(self.user)
        #     else:
        #         self.room.act(self.user, content)
        # except GameActionException:
        #     pass

    def send_information_set(self, event=None):
        self.send_json(RoomSerializer(self.room.data(self.user), context={'user': self.user}).data)
