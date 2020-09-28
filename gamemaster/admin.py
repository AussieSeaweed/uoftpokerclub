from django.contrib import admin
from django.contrib.admin import ModelAdmin, StackedInline

from .models import TicTacToeRoom, Seat


class SeatInline(StackedInline):
    model = Seat

    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(TicTacToeRoom)
class RoomAdmin(ModelAdmin):
    inlines = SeatInline,
