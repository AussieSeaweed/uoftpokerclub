from django.contrib.admin import register, ModelAdmin, StackedInline

from .models import Seat, TicTacToeRoom, NLHERoom


class SeatInline(StackedInline):
    model = Seat

    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False


@register(TicTacToeRoom)
@register(NLHERoom)
class RoomAdmin(ModelAdmin):
    inlines = [SeatInline]
