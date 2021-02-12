from django.urls import path

from django_sos.consumers import LiveConsumer

websocket_urlpatterns = [
    path('live/<str:app_label>/<str:model_name>/<str:pk>/', LiveConsumer.as_asgi()),
]
