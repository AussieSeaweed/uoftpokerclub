from django.urls import path

from gamemaster.consumers import RoomConsumer

websocket_urlpatterns = [
    path('<str:pk>/', RoomConsumer.as_asgi()),
]
