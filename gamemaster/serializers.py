from rest_framework.serializers import ModelSerializer, SerializerMethodField
from json import dumps

from gamemaster.models import Room
from gamemaster.exceptions import SeatNotFoundException
from gamemaster.utils import DefaultToStrJSONEncoder


class RoomSerializer(ModelSerializer):
    game = SerializerMethodField()
    seats = SerializerMethodField()

    def get_game(self, room):
        if room.game is not None:
            try:
                player = room.game.players[room.seat(self.context['user']).index]
            except SeatNotFoundException:
                player = room.game.nature

            return dumps(player.information_set, cls=DefaultToStrJSONEncoder)
        else:
            return None

    @staticmethod
    def get_seats(room):
        return [room.seats[i].information for i in range(room.seat_count)]

    class Meta:
        model = Room
        fields = ['name', 'timeout', 'updated_on', 'game', 'seats']
