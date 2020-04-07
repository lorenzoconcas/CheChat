from django.test import TestCase
from chat.models import *


class MoldesTestCase(TestCase):

    # creazione base test
    def setUp(self):
        # creazione utenti
        Utente.objects.create(nome="Marco", email="marco@iswchat.com", password="1234", cognome="Rossi")
        Utente.objects.create(nome="Antonio", email="antonio@iswchat.com", password="2345", cognome="Verdi")
        Utente.objects.create(nome="Lorena", email="lorena@iswchat.com", password="3456", cognome="Verdi")
        Utente.objects.create(nome="Francesca", email="francesca@iswchat.com", password="4567", cognome="Rossi")

        self.ut1 = Utente.objects.get(email="marco@iswchat.com")
        self.ut2 = Utente.objects.get(email="antonio@iswchat.com")
        self.ut3 = Utente.objects.get(email="lorena@iswchat.com")
        self.ut4 = Utente.objects.get(email="francesca@iswchat.com")

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
        self.assertEqual(self.ut1.email, 'marco@iswchat.com')
        self.assertEqual(self.ut1.cognome, 'Rossi')

    def test_getuser(self):
        self.assertEqual(self.ut1, getuser(1))
        self.assertNotEqual(self.ut1, getuser(12))
        self.assertNotEqual(self.ut2, getuser(1))

    # controllo inserimento rubrica
    def test_insertcontact(self):
        # controllo se è presente quel contatto, aggiungo e riverifico
        self.assertFalse(Rubrica.objects.filter(owner=self.ut1, contatto=self.ut2).exists())
        self.assertEqual("ok", insertcontact(self.ut1, self.ut2))
        self.assertTrue(Rubrica.objects.filter(owner=self.ut1, contatto=self.ut2).exists())
        # controllo il corretto inserimento dei dati
        ut = Utente.objects.get(id=Rubrica.objects.filter(owner=self.ut1, contatto=self.ut2)[0].contatto.id)
        self.assertNotEqual(ut.nome, 'Marco')
        self.assertNotEqual(ut.email, 'marco@iswchat.com')
        self.assertNotEqual(ut.cognome, 'Rossi')
        self.assertEqual(ut.nome, 'Antonio')
        self.assertEqual(ut.email, 'antonio@iswchat.com')
        self.assertEqual(ut.cognome, 'Verdi')
        # provo a reinserire lo stesso contatto
        self.assertNotEqual("ok", insertcontact(self.ut1, self.ut2))

    # controllo rimozione rubrica
    def test_removecontact(self):
        insertcontact(self.ut1, self.ut2)
        # controllo se esiste e poi elimino
        self.assertTrue(Rubrica.objects.filter(owner=self.ut1, contatto=self.ut2).exists())
        self.assertEqual("ok", removecontact(self.ut1, self.ut2))
        # controllo se non è più presente
        self.assertFalse(Rubrica.objects.filter(owner=self.ut1, contatto=self.ut2).exists())
        #provo a cancellare un contatto non presente in rubrica
        self.assertEqual("err", removecontact(self.ut1, self.ut2))

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
        self.assertEqual("err", deletechat(self.ut4.id, self.d.id))

    # controllo in quali chat è presente un utente
    def test_getchats(self):
        list = Partecipanti.objects.filter(contatto=self.ut1)
        filtered_chat_list = getchats(self.ut1)
        list_ids = []
        filtered_ids = []
        for l in list:
            list_ids.append(l.chat_id)

        for l in filtered_chat_list:
            filtered_ids.append(l.chat_id)

        self.assertEqual(list_ids, filtered_ids)

    # controllo invio messaggi DA SISTEMARE
    def test_sendmessage(self):
        mess = Messaggio.objects.filter(chat=self.c, mittente=self.ut1)
        self.assertEqual(mess[0].contenuto, "Ciao")

    # controllo contenuto dell'ultimo messaggio inviato
    def test_getlastmessagecontent(self):
        self.assertEqual("Ciao", getlastmessagecontent(self.c))
        self.assertNotEqual("Bye", getlastmessagecontent(self.c))
        self.assertEqual("", getlastmessagecontent(self.d))

    # controllo ordine dell chat in base all'orario dell'ultimo messaggio
    def test__getorderedchats(self):
        threads = getorderedchats(self.ut1)
        self.assertEqual(threads[0].chat, self.c)
        sendmessage(self.ut1, "Hey", self.d)
        threads = getorderedchats(self.ut1)
        self.assertNotEqual(threads[0].chat, self.c)
        self.assertEqual(threads[0].chat, self.d)

    # controllo se si tratta di un gruppo o di una chat
    def test__getotheruserinchat(self):
        self.assertEqual(getotheruserinchat(self.c, self.ut1), self.ut2)
        self.assertEqual(getotheruserinchat(self.c, self.ut2), self.ut1)
        self.assertNotEqual(getotheruserinchat(self.c, self.ut1), self.ut3)

        self.assertEqual(getotheruserinchat(self.d, self.ut2), "group")
