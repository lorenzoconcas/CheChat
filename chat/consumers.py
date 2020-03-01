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

        req = json.loads(text_data)
        if req['ready']:
            last_messages = []

            c_p_count = len(chat_partecipanti)

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
                                'type': 'new_message',
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
                if len(Partecipanti.objects.filter(contatto_id=current_user)) > c_p_count:
                    chat_partecipanti = Partecipanti.objects.filter(contatto_id=current_user)
                    last_chat = chat_partecipanti.last().chat
                    user = Utente.objects.get(id=current_user)
                    last_chat.nome = last_chat.nome.replace(str(user), ""). replace("-&/&-", "")
                    notifica = json.dumps({
                                'type': 'new_chat',
                                'id': last_chat.id,
                                'name': last_chat.nome,
                            })
                    self.send(notifica)
                    c_p_count += 1


class PushMobile(WebsocketConsumer):
    def connect(self):
        self.accept()

    def disconnect(self, close_code):
        pass

    def receive(self, text_data):

        current_user = int(text_data)
        chat_partecipanti = Partecipanti.objects.filter(contatto_id=1)
        print(text_data)
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
                            'contenuto': ultimo.contenuto,
                            'sender_id': ultimo.mittente.id
                        })
                        print("invio al telefono")
                        self.send(notifica)
                except:
                    update = True
            if update:
                update = False
                for partecipante in chat_partecipanti:
                    last_messages += Messaggio.objects.filter(chat=partecipante.chat)

