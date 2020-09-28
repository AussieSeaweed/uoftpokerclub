from rest_framework import serializers

from community.serializers import UserSerializer
from .models import Room, Seat


class SeatSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    player = serializers.SerializerMethodField()

    def get_player(self, seat):
        return seat.player(self.context["user"])

    class Meta:
        model = Seat
        fields = ["user", "player"]


class RoomSerializer(serializers.ModelSerializer):
    seats = SeatSerializer(many=True)
    actions = serializers.SerializerMethodField()
    user = serializers.SerializerMethodField()

    def get_actions(self, room):
        return room.actions(self.context["user"])

    def get_user(self, room):
        return UserSerializer(instance=self.context["user"]).data

    class Meta:
        model = Room
        fields = ["seats", "context", "actions", "user"]
