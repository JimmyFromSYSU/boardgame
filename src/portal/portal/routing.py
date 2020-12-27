import os
from django.conf.urls import url
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
from channels.auth import AuthMiddlewareStack
from channels.security.websocket import AllowedHostsOriginValidator, OriginValidator
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')

from catan.consumers import CatanConsumer, CatanRoomConsumer

application = ProtocolTypeRouter({
    # "http": get_asgi_application(),
    # Just HTTP for now. (We can add other protocols later.)
    'websocket': AllowedHostsOriginValidator(
        AuthMiddlewareStack(
            URLRouter(
                [
                    url(r'^catan/$', CatanConsumer),
                    url(r'^catan/room/$', CatanRoomConsumer),
                ]
            )
        )
    )
})
