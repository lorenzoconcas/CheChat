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
        session = self.client.session
        session['user_id'] = self.ut1.id
        session.save()

    def test_personalid(self):
        data = {'req':'personal_id'}
        response = self.client.post('/client_reqs/', data, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        json_response = json.loads(response.content)
        result_id = int(json_response[0]['personal_id'])
        self.assertEqual(result_id, self.ut1.id)

    def test_deletechat(self):

        user_ids = []
        user_ids.append(self.ut1.id)
        user_ids.append(self.ut2.id)
        user_ids.append(self.ut3.id)
        data = {'req':'create_chat', 'user_ids_json': user_ids,
                'starting_thread' : 'false', 'base_thread' : 0}
        response = self.client.post('/client_reqs/', data, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        json_response = json.loads(response.content)
        result_id = json_response[0]['result']
        self.assertEqual(result_id, 'ok')