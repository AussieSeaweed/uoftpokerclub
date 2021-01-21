from channels.routing import URLRouter
from django.urls import path

import gamemaster.routing

websocket_urlpatterns = [
    path('', URLRouter(gamemaster.routing.websocket_urlpatterns)),
]
