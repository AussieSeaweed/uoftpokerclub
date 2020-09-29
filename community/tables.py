from django.contrib.auth import get_user_model
from django_tables2.columns import LinkColumn
from django_tables2.tables import Table
from django_tables2.utils import A


class UserTable(Table):
    username = LinkColumn("user-detail", args=[A("pk")])

    class Meta:
        model = get_user_model()
        fields = ["id", "username"]
