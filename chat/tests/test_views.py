from django.test import TestCase, Client
from chat.models import *


class ViewsTestCase(TestCase):
    def setUp(self):
        Utente.objects.create(nome="Marco", email="marco@iswchat.com",  password="1234", cognome="Rossi")
        client = Client()


    def test_getlogin(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)

    def test_login(self):
        mail = "marco@iswchat.com"
        psw = "1234"
        response = self.client.post("/home",
                                    {
                                        'mail': mail,
                                        'password': psw
                                    })
        # se il login riesce ci ritroviamo nella home e non sulla login quindi non viene utilizzata la redirect
        self.assertEqual(response.status_code, 200)

    # simile al test precedente
    def test_login_failed(self):
        response = self.client.post("/home",
                                    {
                                        'mail': "marco@iswchat.com",
                                        'password': "12345"
                                    })
        self.assertEqual(response.status_code, 302)

    # questo test controlla che gli attributi di sessione siano corretti
    def test_session_values(self):
        mail = "marco@iswchat.com"
        psw = "1234"
        response = self.client.post("/home",
                                    {
                                        'mail': mail,
                                        'password': psw
                                    })
        session = self.client.session
        user = Utente.objects.get(email=mail, password=psw)
        self.assertEqual(session['mail'], mail)
        self.assertEqual(session['user_id'], user.id)
        self.assertEqual(session['logged'], True)


     # questo test controlla che gli attributi di sessione siano corretti in caso di login errato
    def test_login_failed_session_values(self):
            mail = "marco@iswchat.com"
            psw = "12345"
            response = self.client.post("/home",
                                        {
                                            'mail': mail,
                                            'password': psw
                                        })
            session = self.client.session
            self.assertEqual(session['validdata'], False)

    def test_logout(self):
        # controlliamo che venga rimandato alla login
        # e che la sessione non esista più
        response = self.client.get("/logout")
        self.assertEqual(response.status_code, 302)
        self.assertEqual(hasattr(response, 'session'), False)