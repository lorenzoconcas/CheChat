from django.test import TestCase, Client
from chat.models import *


class ViewsTestCase(TestCase):
    def setUp(self):
        Users.objects.create(name="Marco", email="marco@iswchat.com", password="1234", surname="Rossi")
        client = Client()

    def test_getlogin(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)

    # test login
    def test_login(self):
        mail = "marco@iswchat.com"
        psw = "1234"
        response = self.client.post("/home",
                                            {
                                                'mail': mail,
                                                'password': psw
                                            })
        # se il login riesce ci ritroviamo nella home e non sulla login quindi
        # non viene utilizzata la redirect
        self.assertEqual(response.status_code, 200)
        #controlliamo anche alcuni valori in sessione
        u = Users.objects.get(email="marco@iswchat.com")
        session = self.client.session
        self.assertEqual(session['mail'], mail)
        self.assertEqual(session['user_id'], u.id)
        self.assertEqual(session['logged'], True)

    def test_login_failed(self):
        response = self.client.post("/home",
                                    {
                                        'mail': "marco@iswchat.com",
                                        'password': "12345"
                                    })
        self.assertEqual(response.status_code, 302)

    # test registrazione
    def test_registration(self):
        mail = "mirko@iswchat.com"
        psw = "1234"
        name = "Mirko"
        family_name = "Argiolas"

        response = self.client.post("/register",
                                    {
                                        "register": True,
                                        'mail': mail,
                                        'password': psw,
                                        'confirm_psw': psw,
                                        'name': name,
                                        'family-name':  family_name
                                    })

        # controllo l'effettiva registrazione dell'utente
        u = Users.objects.get(email=mail)
        self.assertIsNotNone(u)
        self.assertEqual(response.status_code, 302)

    def test_registration_failed_email(self):
        mail = "marco@iswchat.com"
        psw = "1234"
        name = "Mirko"
        family_name = "Argiolas"
        response = self.client.post("/register",
                                    {
                                        "register": True,
                                        'mail': mail,
                                        'password': psw,
                                        'confirm_psw': psw,
                                        'name': name,
                                        'family-name': family_name
                                    })

        self.assertEqual(response.context['response'], "Email già utilizzata")

    def test_registration_failed_psw(self):
        mail = "mirko@iswchat.com"
        psw = "1234"
        name = "Mirko"
        family_name = "Argiolas"
        response = self.client.post("/register",
                                    {
                                        "register": True,
                                        'mail': mail,
                                        'password': psw,
                                        'confirm_psw': psw + "5678",
                                        'name': name,
                                        'family-name': family_name
                                    })

        self.assertEqual(response.context['response'], "Le password non corrispondono")

    def test_registration_failed_empty_fields(self):
        mail = "marco@iswchat.com"
        psw = "1234"
        name = ""
        family_name = ""
        response = self.client.post("/register",
                                    {
                                        "register": True,
                                        'mail': mail,
                                        'password': psw,
                                        'confirm_psw': psw + "5678",
                                        'name': name,
                                        'family-name': family_name
                                    })

        self.assertEqual(response.context['response'], "Compila tutti i campi")

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

    #test logout
    def test_logout(self):
        # controlliamo che venga rimandato alla login
        # e che la sessione non esista più
        response = self.client.get("/logout")
        self.assertEqual(response.status_code, 302)
        self.assertEqual(hasattr(response, 'session'), False)
