from channels.routing import ProtocolTypeRouter, URLRouter
from django.urls import path
from . import consumers

websocket_urlpatterns = [
    path('ws/message/', consumers.FirstConsumer.as_asgi()), 
]

application = ProtocolTypeRouter({
    'websocket': URLRouter(websocket_urlpatterns),
})
