from django.test import TestCase, Client
import json
from chat.models import *


class RequestsTestCase(TestCase):

    def setUp(self):
        self.client = Client()
        Utente.objects.create(nome="Marco", email="marco@iswchat.com", password="1234", cognome="Rossi")
        self.ut1 = Utente.objects.get(email="marco@iswchat.com")
        session = self.client.session
        session['user_id'] = self.ut1.id
        session.save()

    def test_personalid(self):
        data = {'req':'personal_id'}
        response = self.client.post('/client_reqs/', data, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        json_response = json.loads(response.content)
        result_id = int(json_response[0]['personal_id'])
        self.assertEqual(result_id, self.ut1.id)

