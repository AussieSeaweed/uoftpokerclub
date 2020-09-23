from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator

from . import ws_urls

application = ProtocolTypeRouter({
    "websocket": AllowedHostsOriginValidator(AuthMiddlewareStack(URLRouter(ws_urls.urlpatterns))),
})
