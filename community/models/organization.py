from django.contrib.auth import get_user_model
from django.db.models import Model, CharField, ManyToManyField


class Organization(Model):
    name = CharField(max_length=255, unique=True)
    description = CharField(max_length=255, blank=True)
    members = ManyToManyField(get_user_model(), related_name="organizations", blank=True)

    def __str__(self):
        return self.name
