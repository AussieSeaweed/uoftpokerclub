from rest_framework.serializers import ModelSerializer, SerializerMethodField

from community.serializers import UserSerializer
from .models import Room, Seat


class SeatSerializer(ModelSerializer):
    user = UserSerializer()
    player = SerializerMethodField()

    def get_player(self, seat):
        return seat.player(self.context["user"])

    class Meta:
        model = Seat
        fields = ["user", "status", "stats", "player"]


class RoomSerializer(ModelSerializer):
    user = SerializerMethodField()
    seats = SeatSerializer(many=True)
    actions = SerializerMethodField()

    def get_user(self, room):
        return UserSerializer(instance=self.context["user"]).data if self.context["user"].is_authenticated else None

    def get_actions(self, room):
        return room.actions(self.context["user"])

    class Meta:
        model = Room
        fields = ["user", "updated_on", "timeout", "config", "seats", "context", "actions"]
