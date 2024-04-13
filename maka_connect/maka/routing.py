# chat/routing.py
from django.urls import re_path

from . import consumers

websocket_urlpatterns = [
    re_path(r"ws/event/", consumers.ChatConsumer.as_asgi()),
    re_path(r"ws/unreadmessages/", consumers.LikesConsumer.as_asgi()),
]

"""

from . import consumers

channel_routing = {
    'websocket.connect': consumers.ws_connect,
    'websocket.receive': consumers.ws_receive,
    'websocket.disconnect': consumers.ws_disconnect,
}

"""