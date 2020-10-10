from django_tables2.columns import LinkColumn, Column
from django_tables2.tables import Table
from django_tables2.utils import A

from .models import Room


class RoomTable(Table):
    name = LinkColumn("room-detail", args=[A("pk")])
    description = Column(orderable=False)
    status = Column(orderable=False, accessor="users")

    @staticmethod
    def render_status(value):
        return f"{len(value)} Online"

    class Meta:
        model = Room
        fields = ["name", "description", "status"]
