from datetime import datetime
from time import sleep
from chat.models import *
from channels.generic.websocket import WebsocketConsumer
import json


class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()

    def disconnect(self, close_code):
        pass

    def receive(self, text_data):
        while True:
            self.send(text_data=json.dumps({
                'message': datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            }))


class PushMessages(WebsocketConsumer):
    def connect(self):
        self.accept()


    def disconnect(self, close_code):
        pass

    def receive(self, text_data):
        session = self.scope["session"]
        current_user = session['user_id']
        chat_partecipanti = Partecipanti.objects.filter(contatto_id=current_user)

        last_messages = []
        chats = []
        for partecipante in chat_partecipanti:
            last_messages += Messaggio.objects.filter(chat=partecipante.chat)
        update = False
        while True:
            for partecipante in chat_partecipanti:
                messaggi = Messaggio.objects.filter(chat=partecipante.chat)
                ultimo = messaggi.last()
                contiene_msg = ultimo in last_messages
                try:
                    if not contiene_msg and not ultimo.mittente.id == current_user:
                        contiene_msg = True
                        update = True
                        notifica = json.dumps({
                            'chat_id': ultimo.chat.id,
                            'mittente': ultimo.mittente.__str__(),
                            'dataora': ultimo.dataora.strftime("%Y-%m-%d %H:%M:%S"),
                            'contenuto': ultimo.contenuto
                        })
                        self.send(notifica)
                except:
                    update = True
            if update:
                update = False
                for partecipante in chat_partecipanti:
                    last_messages += Messaggio.objects.filter(chat=partecipante.chat)

