from rest_framework.serializers import ModelSerializer, SerializerMethodField

from gamemaster.models import Room
from gamemaster.exceptions import SeatNotFoundException
from gamemaster.utils import InformationSetJSONEncoder


class RoomSerializer(ModelSerializer):
    information_set_encoder = InformationSetJSONEncoder()

    game = SerializerMethodField()
    seats = SerializerMethodField()

    def get_game(self, room):
        if room.game is not None:
            try:
                player = room.game.players[room.seat(self.context['user']).index]
            except SeatNotFoundException:
                player = room.game.nature

            return self.information_set_encoder.encode(player.information_set)
        else:
            return None

    @staticmethod
    def get_seats(room):
        return [room.seats[i].information for i in range(room.seat_count)]

    class Meta:
        model = Room
        fields = ['name', 'timeout', 'updated_on', 'game', 'seats']
