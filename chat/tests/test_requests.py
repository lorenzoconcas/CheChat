from django.test import TestCase, Client
import json
from chat.models import *


class RequestsTestCase(TestCase):

    def setUp(self):
        self.client = Client()
        Utente.objects.create(nome="Marco", email="marco@iswchat.com", password="1234", cognome="Rossi")
        Utente.objects.create(nome="Antonio", email="anto@iswchat.com", password="2345", cognome="Verdi")
        Utente.objects.create(nome="Lorena", email="lorena@iswchat.com", password="3456", cognome="Verdi")
        self.ut1 = Utente.objects.get(email="marco@iswchat.com")
        self.ut2 = Utente.objects.get(email="anto@iswchat.com")
        self.ut3 = Utente.objects.get(email="lorena@iswchat.com")

        # questa parte va rivista (ricopiata) nei test che prevedono un id utente differente
        session = self.client.session
        session['user_id'] = self.ut1.id
        session.save()

    # test aggiunta contatto
    def test_add_contact(self):
        data = {'req': 'add_contact', 'mail': self.ut2.email}
        response = self.client.post('/client_reqs/', data, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertNotEqual(response.status_code, 302)
        json_response = json.loads(response.content)[0]
        self.assertEqual(json_response['result'], 'ok')
        self.assertEqual(json_response['id'], str(self.ut2.id))
        self.assertEqual(json_response['name'], str(self.ut2))

    def test_add_contact_fail_same_user(self):
        data = {'req': 'add_contact', 'mail': self.ut1.email}
        response = self.client.post('/client_reqs/', data, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertNotEqual(response.status_code, 302)
        json_response = json.loads(response.content)[0]
        self.assertEqual(json_response['result'], 'err')
        self.assertEqual(json_response['error'], 'Non si può aggiungere se stessi')

    def test_add_contact_fail_no_user(self):
        data = {'req': 'add_contact', 'mail': 'cieufuweiur'}
        response = self.client.post('/client_reqs/', data, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertNotEqual(response.status_code, 302)
        json_response = json.loads(response.content)[0]
        self.assertEqual(json_response['result'], 'err')
        self.assertEqual(json_response['error'], 'Utente non trovato')

    def test_add_contact_fail_already_added(self):
        Rubrica.objects.create(owner=self.ut1, contatto=self.ut2)
        data = {'req': 'add_contact', 'mail': self.ut2.email}
        response = self.client.post('/client_reqs/', data, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertNotEqual(response.status_code, 302)
        json_response = json.loads(response.content)[0]
        self.assertEqual(json_response['result'], 'err')
        self.assertEqual(json_response['error'], 'Utente già in rubrica')

    #test rimozione contatto
    def test_remove_contact(self):
        Rubrica.objects.create(owner=self.ut1, contatto=self.ut2)
        data = {'req': 'remove_contact', 'remove_id': self.ut2.id}
        response = self.client.post('/client_reqs/', data, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertNotEqual(response.status_code, 302)
        json_response = json.loads(response.content)[0]
        self.assertEqual(json_response['result'], 'ok')

    def test_remove_contact_fail(self):
        data = {'req': 'remove_contact', 'remove_id': self.ut2.id}
        response = self.client.post('/client_reqs/', data, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertNotEqual(response.status_code, 302)
        json_response = json.loads(response.content)[0]
        self.assertEqual(json_response['result'], 'err')

    #test creazione chat
    def test_create_chat(self):
        user_ids = []
        user_ids.append(str(self.ut2.id))
        user_ids = json.dumps(user_ids)
        data = {'req': 'create_chat', 'user_ids_json': user_ids,
                'adding_to_thread': 'false', 'base_thread': 0}
        response = self.client.post('/client_reqs/', data, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        result = json.loads(response.content)[0]['result']
        self.assertEqual(result, 'ok')

    def test_create_group_chat(self):
        user_ids = []
        user_ids.append(str(self.ut1.id))
        user_ids.append(str(self.ut2.id))
        user_ids.append(str(self.ut3.id))
        user_ids = json.dumps(user_ids)
        data = {'req':'create_chat', 'user_ids_json': user_ids,
                'adding_to_thread' : 'false', 'base_thread' : 0}
        response = self.client.post('/client_reqs/', data, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        json_response = json.loads(response.content)
        result = json_response[0]['result']
        self.assertEqual(result, 'ok')

    #test cancellazione chat
    def test_delete_chat(self):
        c = createchat(self.ut1, [self.ut2.id])
        data = {'req': 'delete_chat', 'chat_id': c.id}
        response = self.client.post('/client_reqs/', data, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        result = json.loads(response.content)[0]['delete']
        self.assertEqual(result, "ok")

    def test_delete_chat_fail_chat_not_exists(self):
        data = {'req': 'delete_chat', 'chat_id': 2}
        response = self.client.post('/client_reqs/', data, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        result = json.loads(response.content)[0]['delete']
        self.assertEqual(result, "err")

    def test_delete_chat_fail_not_in_chat(self):
        c = createchat(self.ut3, [self.ut2.id])
        data = {'req': 'delete_chat', 'chat_id': c.id}
        response = self.client.post('/client_reqs/', data, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        result = json.loads(response.content)[0]['delete']
        self.assertEqual(result, "err")

    #test caricamento messaggi
    def test_get_all_messages(self):
        chat = createchat(self.ut1, [self.ut2.id])
        for i in range(5):
            sendmessage(self.ut1, "Messaggio : " + str(i), chat)
            sendmessage(self.ut2, "Risposta : " + str(i), chat)

        data = {'req': 'get_all_messages', 'chat_id': chat.id}
        response = self.client.post('/client_reqs/', data, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertNotEqual(response.status_code, 302)
        #significa che la chat è piena (volendo si può controllare il contenuto)
        self.assertNotEqual(response.content, "[]")

    def test_get_all_messages_fail_not_in_chat(self):
        session = self.client.session
        session['user_id'] = self.ut3.id
        session.save()

        chat = createchat(self.ut1, [self.ut2.id])
        for i in range(5):
            sendmessage(self.ut1, "Messaggio : " + str(i), chat)
            sendmessage(self.ut2, "Risposta : " + str(i), chat)

        data = {'req': 'get_all_messages', 'chat_id': chat.id}
        response = self.client.post('/client_reqs/', data, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertNotEqual(response.status_code, 302)
        result = json.loads(response.content)
        # agli utenti non partecipanti tale chat risulta vuota (sia che esista sia che non esista)
        self.assertEqual(result, [])

    def test_get_all_messages_fail_chat_not_exist(self):
        # essendo vuoto il db siamo sicuri che non ci sia la chat con id 2 (e nemmeno 1 ecc)
        data = {'req': 'get_all_messages', 'chat_id': 2}
        response = self.client.post('/client_reqs/', data, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertNotEqual(response.status_code, 302)
        result = json.loads(response.content)
        # agli utenti non partecipanti tale chat risulta vuota (sia che esista sia che non esista)
        self.assertEqual(result, [])

    #test invio messaggi
    def test_send_message(self):
        c = createchat(self.ut1, [self.ut2.id])
        data = {'req': 'send_message', 'msg': 'Prova',
                'chat_id': c.id}
        response = self.client.post('/client_reqs/', data, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.content, b'sent')

    def test_send_message_not_in_chat(self):
        session = self.client.session
        session['user_id'] = self.ut3.id
        session.save()
        c = createchat(self.ut1, [self.ut2.id])
        data = {'req': 'send_message', 'msg': 'Prova',
                'chat_id': c.id}
        response = self.client.post('/client_reqs/', data, HTTP_X_REQUESTED_WITH='XMLHttpRequest')

        self.assertEqual(response.content, b'not_allowed')

    def test_send_message_chat_not_exist(self):

        data = {'req': 'send_message', 'msg': 'Prova',
                'chat_id': 2}
        response = self.client.post('/client_reqs/', data, HTTP_X_REQUESTED_WITH='XMLHttpRequest')

        self.assertEqual(response.content, b'not_allowed')

    #test get chat icon
    def test_get_chat_icon(self):
        c = createchat(self.ut1, [self.ut2.id])
        data = {'req': 'get_chat_icon', 'chat_id': c.id}
        response = self.client.post('/client_reqs/', data, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.content, b'static/chat/icons/user_icon_2.png')

    def test_get_group_chat_icon(self):
        c = createchat(self.ut1, [self.ut2.id, self.ut2.id])
        data = {'req': 'get_chat_icon', 'chat_id': c.id}
        response = self.client.post('/client_reqs/', data, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.content, b'static/chat/icons/user_group.png')