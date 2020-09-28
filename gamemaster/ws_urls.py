from django.urls import path

from .consumers import RoomConsumer

urlpatterns = [
    path("rooms/<int:pk>/", RoomConsumer),
]
