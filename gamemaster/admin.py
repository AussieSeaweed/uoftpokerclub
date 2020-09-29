from django.contrib.admin import register, ModelAdmin, StackedInline

from .models import TicTacToeRoom, Seat


class SeatInline(StackedInline):
    model = Seat

    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False


@register(TicTacToeRoom)
class RoomAdmin(ModelAdmin):
    inlines = [SeatInline]
