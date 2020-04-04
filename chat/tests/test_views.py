from django.test import TestCase
from chat.models import *


class ViewsTestCase(TestCase):
    def setUp(self):
        # creazione utenti
        Utente.objects.create(nome="Marco", email="Marco@iswchat.com", password="1234", cognome="Rossi")
        Utente.objects.create(nome="Antonio", email="Anto@iswchat.com", password="2345", cognome="Verdi")
        Utente.objects.create(nome="Lorena", email="Lorena@iswchat.com", password="3456", cognome="Verdi")
        Utente.objects.create(nome="Francesca", email="Francesca@iswchat.com", password="4567", cognome="Rossi")
        self.ut1 = Utente.objects.get(nome="Marco")
        self.ut2 = Utente.objects.get(nome="Antonio")
        self.ut3 = Utente.objects.get(nome="Lorena")
        self.ut4 = Utente.objects.get(nome="Francesca")

        # creazione chat
        ids = []
        ids.append(int(self.ut1.id))
        self.c = createchat(self.ut2, ids)
        ids.append(int(self.ut2.id))
        self.d = createchat(self.ut3, ids)

        # invio messagio
        sendmessage(self.ut1, "Ciao", self.c)

        # controllo se i dati inseriti nell'oggetto Utente sono corretti

    def test_utente(self):
        self.assertEqual(self.ut1.nome, 'Marco')
        self.assertEqual(self.ut1.email, 'Marco@iswchat.com')
        self.assertEqual(self.ut1.email, 'Marco@iswchat.com')
        self.assertEqual(self.ut1.cognome, 'Rossi')



