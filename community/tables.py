from itertools import count

from django.contrib.auth import get_user_model
from django_tables2.columns import Column, LinkColumn
from django_tables2.tables import Table
from django_tables2.utils import A

from .models import Organization


class CountedMixin(Table):
    row_number = Column(empty_values=(), verbose_name="#", orderable=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.counter = count(1)

    def render_row_number(self):
        return next(self.counter)


class UserTable(CountedMixin, Table):
    username = LinkColumn("user-detail", args=[A("pk")])
    career__nlhestat__payoffs = Column(verbose_name="NLHE Profit")

    class Meta:
        model = get_user_model()
        fields = ["row_number", "username", "career__nlhestat__payoffs"]


class OrganizationTable(CountedMixin, Table):
    name = LinkColumn("organization-detail", args=[A("pk")])

    class Meta:
        model = Organization
        fields = ["row_number", "name"]
