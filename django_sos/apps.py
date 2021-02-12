from importlib import import_module

from django.apps import AppConfig
from django.conf import settings
from django.conf.urls.static import static


class DjangoSOSConfig(AppConfig):
    """DjangoSOSConfig is the class for the django-sos app configuration."""

    name = 'django_sos'

    def ready(self):
        """Automatically hosts media files during debugging, and links signals.

        :return: None
        """
        from django_sos.signals import setup

        setup()

        try:
            if settings.DEBUG_SERVE_MEDIA and settings.DEBUG and settings.MEDIA_ROOT:
                import_module(settings.ROOT_URLCONF).urlpatterns.extend(static(
                    settings.MEDIA_URL,
                    document_root=settings.MEDIA_ROOT,
                ))
        except AttributeError:
            pass
