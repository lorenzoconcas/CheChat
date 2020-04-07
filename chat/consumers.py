from chat.models import *
from channels.generic.websocket import WebsocketConsumer
import json


class PushMessages(WebsocketConsumer):
    def connect(self):
        self.accept()

    def disconnect(self, close_code):
        pass

    def receive(self, text_data):
        session = self.scope["session"]
        current_user = session['user_id']

        try:
            chat_partecipanti = Partecipants.objects.filter(contact_id=current_user) # le chat a cui partecipa l'utente
        except models.ObjectDoesNotExist:
            return

        req = json.loads(text_data)
        if req['ready']:
            last_messages = []  # gli ultimi messaggi delle chat a cui partecipa
            c_p_count = len(chat_partecipanti)  # il conto delle chat a cui partecipa

            for partecipante in chat_partecipanti:
                last_messages += Messages.objects.filter(chat=partecipante.chat)  # per ogni chat a prendiamo
                # gli ultimi messaggi
            update = False  # servirà per sapere se aggiornare la variabile
            while True:
                for partecipante in chat_partecipanti:  # per ogni chat a cui partecipa
                    messages = Messages.objects.filter(chat=partecipante.chat)  # carichiamo i messaggi di quella chat
                    last = messages.last()  # prendiamo l'ultimo
                    contiene_msg = last in last_messages  # verifichiamo se abbiamo già notificato l'utente del msg
                    if not contiene_msg and last is not None and last.sender.id is not None:
                        # se non l'abbiamo fatto
                        contiene_msg = True
                        if not current_user == last.sender.id:
                            is_inviato = 'false'
                            mittente = str(last.sender)
                            notifica = json.dumps({  # prepariamo il messaggio per il client
                                'type': 'new_message',
                                'chat_id': last.chat.id,
                                'sender': mittente,
                                'time': last.time.strftime("%Y-%m-%d %H:%M:%S"),
                                'content': last.content,
                                'sent':  is_inviato

                             })
                            self.send(notifica)
                        update = True  # al prossimo ciclo controlliamo se ci sono nuovi messaggi
                    else:
                        update = True  # significa che la chat non è ancora stata notificata

                if update:  # aggiorniamo la variabile contente l'ultimo msg delle chat a cui partecipa
                    update = False
                    for partecipante in chat_partecipanti:
                        last_messages += Messages.objects.filter(chat=partecipante.chat)
                # se il numero delle chat in cui è coinvolto aumenta notifico il client
                if len(Partecipants.objects.filter(contact_id=current_user)) > c_p_count:
                    chat_partecipanti = Partecipants.objects.filter(contact_id=current_user)
                    last_chat = chat_partecipanti.last().chat
                    user = Users.objects.get(id=current_user)
                    last_chat.name = last_chat.name.replace(str(user), "")
                    if last_chat.name.startswith("Gruppo"):
                        thread_icon = '/static/chat/icons/user_group.png'
                    else:
                        other = getotheruserinchat(last_chat, user)
                        if other == '':
                            thread_icon = '/static/chat/icons/user_icon_1.png'
                        else:
                            img_id = int(other.id) % 5
                            if img_id == 0:
                                img_id = 1
                            thread_icon = '/static/chat/icons/user_icon_' + str(img_id) + '.png'
                    notifica = json.dumps({
                                'type': 'new_chat',
                                'id': last_chat.id,
                                'name': last_chat.name,
                                'thread_icon': thread_icon
                            })
                    if not last_chat.creator == user:  # se è stata creata dall'utente è già nella sua list
                        # questo rimuove la sincronizzazione delle chat fra dispositivi,
                        # ma è sicuro che la chat venga aggiunta graficamente
                        self.send(notifica)
                    c_p_count = len(chat_partecipanti)  # lo aggiorno in modo da non avere
                    # conflitti con la cancellazione delle chat
