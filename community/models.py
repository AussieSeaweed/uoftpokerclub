from annoying.fields import AutoOneToOneField
from django.contrib.auth import get_user_model
from django.db import models


class Profile(models.Model):
    user = AutoOneToOneField(get_user_model(), unique=True, on_delete=models.CASCADE)

    description = models.TextField(blank=True)

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
