from django.urls import path

from gamemaster.consumers import RoomConsumer

websocket_urlpatterns = [
    path('rooms/<int:pk>/', RoomConsumer),
]
