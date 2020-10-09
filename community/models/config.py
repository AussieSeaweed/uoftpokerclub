from annoying.fields import AutoOneToOneField
from django.contrib.auth import get_user_model
from django.db.models import Model, CASCADE


class Config(Model):
    user = AutoOneToOneField(get_user_model(), unique=True, on_delete=CASCADE)

    def __str__(self):
        return self.user.username
