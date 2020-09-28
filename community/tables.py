from django.contrib.auth import get_user_model
from django_tables2 import tables, columns
from django_tables2.utils import A


class UserTable(tables.Table):
    username = columns.LinkColumn("user-detail", args=[A("pk")])

    class Meta:
        model = get_user_model()
        fields = ["id", "username"]
