from django.contrib.admin import register, ModelAdmin

from gamemaster.models import TicTacToeRoom


@register(TicTacToeRoom)
class RoomAdmin(ModelAdmin):
    pass
