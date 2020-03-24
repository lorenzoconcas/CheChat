from chat.models import *
from channels.generic.websocket import WebsocketConsumer
from django.core import exceptions
import json


class PushMessages(WebsocketConsumer):
    def connect(self):
        self.accept()
        # async_to_sync(self.channel_layer.group_add)("push", self.channel_name)

    def disconnect(self, close_code):
        pass

    def receive(self, text_data):
        session = self.scope["session"]
        current_user = session['user_id']

        try:
            chat_partecipanti = Partecipanti.objects.filter(contatto_id=current_user) # le chat a cui partecipa l'utente
        except models.ObjectDoesNotExist:
            return

        req = json.loads(text_data)
        if req['ready']:
            last_messages = []  # gli ultimi messaggi delle chat a cui partecipa
            c_p_count = len(chat_partecipanti)  # il conto delle chat a cui partecipa

            for partecipante in chat_partecipanti:
                last_messages += Messaggio.objects.filter(chat=partecipante.chat)  # per ogni chat a prendiamo
                # gli ultimi messaggi
            update = False  # servirà per sapere se aggiornare la variabile
            while True:
                for partecipante in chat_partecipanti:  # per ogni chat a cui partecipa
                    messaggi = Messaggio.objects.filter(chat=partecipante.chat)  # carichiamo i messaggi di quella chat
                    ultimo = messaggi.last()  # prendiamo l'ultimo
                    contiene_msg = ultimo in last_messages  # verifichiamo se abbiamo già notificato l'utente del msg
                    if not contiene_msg and ultimo is not None and ultimo.mittente.id is not None:
                        # se non l'abbiamo fatto
                        contiene_msg = True
                        if current_user == ultimo.mittente.id:
                            is_inviato = 'True'
                            mittente = ""
                        else:
                            is_inviato = 'false'
                            mittente = str(ultimo.mittente)

                        update = True  # al prossimo ciclo controlliamo se ci sono nuovi messaggi
                        notifica = json.dumps({  # prepariamo il messaggio per il client
                            'type': 'new_message',
                            'chat_id': ultimo.chat.id,
                            'mittente': mittente,
                            'dataora': ultimo.dataora.strftime("%Y-%m-%d %H:%M:%S"),
                            'contenuto': ultimo.contenuto,
                            'inviato':  is_inviato

                         })
                        self.send(notifica)
                    else:
                        update = True  # significa che la chat non è ancora stata notificata

                if update:  # aggiorniamo la variabile contente l'ultimo msg delle chat a cui partecipa
                    update = False
                    for partecipante in chat_partecipanti:
                        last_messages += Messaggio.objects.filter(chat=partecipante.chat)
                # se il numero delle chat in cui è coinvolto aumenta notifico il client
                if len(Partecipanti.objects.filter(contatto_id=current_user)) > c_p_count:
                    chat_partecipanti = Partecipanti.objects.filter(contatto_id=current_user)
                    last_chat = chat_partecipanti.last().chat
                    user = Utente.objects.get(id=current_user)
                    last_chat.nome = last_chat.nome.replace(str(user), "")
                    notifica = json.dumps({
                                'type': 'new_chat',
                                'id': last_chat.id,
                                'name': last_chat.nome,
                            })
                    self.send(notifica)
                    c_p_count = len(chat_partecipanti)  # lo aggiorno in modo da non avere
                    # conflitti con la cancellazione delle chat


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

