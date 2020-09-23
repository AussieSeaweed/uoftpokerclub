from channels.routing import URLRouter
from django.urls import path

import gamemaster.ws_urls

urlpatterns = [
    path("gamemaster/", URLRouter(gamemaster.ws_urls.urlpatterns)),
]
