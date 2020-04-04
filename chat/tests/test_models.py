from django.test import TestCase
from chat.models import *


class MoldesTestCase(TestCase): # <- modifica

    # creazione base test
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

        #creazione chat
        ids = []
        ids.append(int(self.ut1.id))
        self.c = createchat(self.ut2, ids)
        ids.append(int(self.ut2.id))
        self.d = createchat(self.ut3, ids)

        #invio messagio
        sendmessage(self.ut1, "Ciao", self.c)

    # controllo se i dati inseriti nell'oggetto Utente sono corretti
    def test_utente(self):
        self.assertEqual(self.ut1.nome, 'Marco')
        self.assertEqual(self.ut1.email, 'Marco@iswchat.com')
        self.assertEqual(self.ut1.email, 'Marco@iswchat.com')
        self.assertEqual(self.ut1.cognome, 'Rossi')

    def test_getuser(self):
        self.assertEqual(self.ut1, getuser(1))

    # controllo inserimento rubrica
    def test_insertcontact(self):
        # controllo se è presente quel contatto, aggiungo e riverifico
        self.assertFalse(Rubrica.objects.filter(owner=self.ut1, contatto=self.ut2).exists())
        insertcontact(self.ut1, self.ut2)
        self.assertTrue(Rubrica.objects.filter(owner=self.ut1, contatto=self.ut2).exists())

    # controllo rimozione rubrica
    def test_removecontact(self):
        insertcontact(self.ut1, self.ut2)
        # controllo se esiste e poi elimino
        self.assertTrue(Rubrica.objects.filter(owner=self.ut1, contatto=self.ut2).exists())
        removecontact(self.ut1, self.ut2)
        # controllo se non è più presente
        self.assertFalse(Rubrica.objects.filter(owner=self.ut1, contatto=self.ut2).exists())

    # controlli creazione chat e gruppi
    def test_createchat(self):
        self.assertTrue(Chat.objects.filter(creatore=self.ut2.id).exists())
        self.assertFalse(Chat.objects.filter(creatore=self.ut1.id).exists())
        self.assertEqual(self.c.nome, str(self.ut2) + " " + str(self.ut1))
        self.assertEqual(str(self.c.creatore), str(self.ut2))

        self.assertTrue(Chat.objects.filter(creatore=self.ut3.id).exists())
        self.assertEqual(self.d.nome, "Gruppo: " + str(self.ut1) + ", " + str(self.ut2) + ", " + str(self.ut3))
        self.assertEqual(str(self.d.creatore), str(self.ut3))

    # controllo aggiunta di un membro da una chat
    def test_addusertochat(self):
        self.assertFalse(Partecipanti.objects.filter(chat=self.d, contatto=self.ut4).exists())
        addusertochat(self.d, self.ut4)
        self.assertTrue(Partecipanti.objects.filter(chat=self.d, contatto=self.ut4).exists())

    # controllo la corretta cancellazione di un utente da una chat
    def test_deletechat(self):
        addusertochat(self.d, self.ut4)
        self.assertTrue(Partecipanti.objects.filter(chat=self.d, contatto=self.ut4).exists())
        deletechat(self.ut4.id, self.d.id)
        self.assertFalse(Partecipanti.objects.filter(chat=self.d, contatto=self.ut4).exists())
        # provo a cancellare un utente non inserito in quella chat
        try:
            deletechat(self.ut4.id, self.d.id)
            self.assertTrue(False)
        except:
            self.assertTrue(True)

    # controllo chat
    def test_getchat(self):
        self.assertEqual(getchat(self.c.id), self.c)
        try:
            self.assertEqual(getchat(0), self.c)
            self.assertTrue(False)
        except:
            self.assertTrue(True)

    # controllo in quali chat è presente un utente DA SISTEMARE
    def test_getchats(self):
        list = Partecipanti.objects.filter(contatto=self.ut1)
        # da sistemare
        #self.assertEqual(list, getchats(self.ut1))
        print(str(list)) # stampa con andate a capo
        # print(getchats(self.ut1))

    # controllo invio messaggi DA SISTEMARE
    def test_sendmessage(self):
        mess = Messaggio.objects.filter(chat=self.c, mittente=self.ut1)
        self.assertEqual(mess[0].contenuto, "Ciao")

    # controllo contenuto dell'ultimo messaggio inviato
    def test_getlastmessagecontent(self):
        self.assertEqual("Ciao", getlastmessagecontent(self.c))
        self.assertNotEqual("Bye", getlastmessagecontent(self.c))
        self.assertEqual("", getlastmessagecontent(self.d))

    #getorderedchats

    #getotheruserinchat

    # controllo login/logout

    # controllo apertura chat

    # controllo invio dei messaggi (destinatario e contenuto)

    # controllo se un utente esterno può accedere ad una chat non sua

