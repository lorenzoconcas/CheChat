from django.urls import re_path

from . import consumers

websocket_urlpatterns = [
    # questi sono gli indirizzi dei websockets
    re_path('ws/push_messages', consumers.PushMessages),  # per la pagina web
    re_path('ws/push_mobile', consumers.PushMobile),  # per l'app nativa
]