from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    # questi sono gli indirizzi dei websockets
    # sono usati per le notifiche push
    re_path('ws/push_messages', consumers.PushMessages),
]
