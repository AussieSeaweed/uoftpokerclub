from django.contrib.admin import register, ModelAdmin

from gamemaster.models import TTTRoom


@register(TTTRoom)
class RoomAdmin(ModelAdmin):
    pass
