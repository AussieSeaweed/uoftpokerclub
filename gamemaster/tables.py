from django_tables2 import tables, columns
from django_tables2.utils import A

from .models import Room


class RoomTable(tables.Table):
    name = columns.LinkColumn("room-detail", args=[A("pk")])
    description = columns.Column(orderable=False)
    status = columns.Column(orderable=False)

    class Meta:
        model = Room
        fields = ["id"]
