from django.urls import re_path

from . import consumers

websocket_urlpatterns = [
    re_path('ws/testsocket', consumers.ChatConsumer),
    re_path('ws/push_messages', consumers.PushMessages),
]