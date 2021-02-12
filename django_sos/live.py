from collections import defaultdict

from django.contrib.contenttypes.models import ContentType
from django_sos.exceptions import UnregisteredModelException

_live_consumers = defaultdict(lambda: defaultdict(set))
_serializers = {}


def register(model, serializer):
    _serializers[ContentType.objects.get_for_model(model)] = serializer


def get_live_consumers(instance):
    return _live_consumers[ContentType.objects.get_for_model(instance)][instance.pk]


def get_live_data(instance):
    model_live = _serializers[ContentType.objects.get_for_model(instance)]

    if model_live is None:
        raise UnregisteredModelException()
    else:
        return model_live
