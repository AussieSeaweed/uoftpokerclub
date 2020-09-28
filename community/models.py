from annoying.fields import AutoOneToOneField
from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse
from django_gravatar.helpers import get_gravatar_url


class Profile(models.Model):
    user = AutoOneToOneField(get_user_model(), unique=True, on_delete=models.CASCADE)

    @property
    def url(self):
        return reverse("user-detail", kwargs={"pk": self.user.id})

    @property
    def gravatar_url(self):
        return get_gravatar_url(self.user.email, 500)

    def __str__(self):
        return self.user.username


class Config(models.Model):
    user = AutoOneToOneField(get_user_model(), unique=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username


class Career(models.Model):
    user = AutoOneToOneField(get_user_model(), unique=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username
