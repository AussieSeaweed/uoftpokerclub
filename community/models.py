from annoying.fields import AutoOneToOneField
from django.contrib.auth import get_user_model
from django.db.models import Model, CASCADE
from django.urls import reverse
from django_gravatar.helpers import get_gravatar_url


class Profile(Model):
    user = AutoOneToOneField(get_user_model(), unique=True, on_delete=CASCADE)

    @property
    def url(self):
        return reverse("user-detail", kwargs={"pk": self.user.id})

    @property
    def gravatar_url(self):
        return get_gravatar_url(self.user.email, 500)

    def __str__(self):
        return self.user.username


class Config(Model):
    user = AutoOneToOneField(get_user_model(), unique=True, on_delete=CASCADE)

    def __str__(self):
        return self.user.username


class Career(Model):
    user = AutoOneToOneField(get_user_model(), unique=True, on_delete=CASCADE)

    def __str__(self):
        return self.user.username
