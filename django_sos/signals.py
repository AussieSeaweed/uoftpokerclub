from django.db.models.signals import post_save
from django.dispatch import receiver


@receiver(post_save)
def send_model_live(instance, **kwargs):
    pass


def setup():
    pass
