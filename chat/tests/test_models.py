from django.test import TestCase
from chat.models import *


class ModelsTestCase(TestCase):

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

        # creazione chat
        ids = []
        ids2 = []
        ids.append(int(self.ut1.id))
        ids2.append(int(self.ut3.id))
        self.c = createchat(self.ut2, ids)
        ids.append(int(self.ut2.id))
        self.d = createchat(self.ut3, ids)
        self.e = createchat(self.ut4, ids2)

        # invio messagio
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
        result = insertcontact(self.ut1, self.ut2)
        self.assertNotEqual(result, "ok")

    # controllo rimozione rubrica
    def test_removecontact(self):
        insertcontact(self.ut1, self.ut2)
        # controllo se esiste e poi elimino
        self.assertTrue(Rubrica.objects.filter(owner=self.ut1, contatto=self.ut2).exists())
        result = removecontact(self.ut1, self.ut2)
        self.assertEqual(result, "ok")
        # controllo se non è più presente
        self.assertFalse(Rubrica.objects.filter(owner=self.ut1, contatto=self.ut2).exists())
        # provo a cancellare un contatto non presente in rubrica
        result = removecontact(self.ut1, self.ut2)
        self.assertEqual(result, "err")

    # controlli creazione chat e gruppi
    def test_createchat(self):
        # chat normale
        self.assertTrue(Chat.objects.filter(creatore=self.ut2.id).exists())
        self.assertFalse(Chat.objects.filter(creatore=self.ut1.id).exists())
        result = str(self.ut2) + " " + str(self.ut1)
        self.assertEqual(result, self.c.nome)
        self.assertEqual(str(self.c.creatore), str(self.ut2))
        # chat di gruppo
        self.assertTrue(Chat.objects.filter(creatore=self.ut3.id).exists())
        result = "Gruppo: " + str(self.ut1) + ", " + str(self.ut2) + ", " + str(self.ut3)
        self.assertEqual(result, self.d.nome)
        self.assertEqual(str(self.d.creatore), str(self.ut3))

    # controllo aggiunta di un membro da una chat
    def test_addusertochat(self):
        # controllo prima se è presente nella chat, lo inserisco e ripeto la verifica
        self.assertFalse(Partecipanti.objects.filter(chat=self.d, contatto=self.ut4).exists())
        addusertochat(self.d, self.ut4)
        self.assertTrue(Partecipanti.objects.filter(chat=self.d, contatto=self.ut4).exists())
        # cosa succede se cerco di inserire un utente già presente?
        result = addusertochat(self.d, self.ut4)
        self.assertEqual(result, "err")

    # controllo la corretta cancellazione di un utente da una chat
    def test_deletechat(self):
        addusertochat(self.d, self.ut4)
        self.assertTrue(Partecipanti.objects.filter(chat=self.d, contatto=self.ut4).exists())
        result = deletechat(self.ut4.id, self.d.id)
        self.assertNotEqual(result, "err")
        self.assertFalse(Partecipanti.objects.filter(chat=self.d, contatto=self.ut4).exists())
        # provo a cancellare un utente non inserito in quella chat
        result = deletechat(self.ut4.id, self.d.id)
        self.assertEqual(result, "err")

    # controllo in quali chat è presente un utente
    def test_getchats(self):
        list_chats = Partecipanti.objects.filter(contatto=self.ut1)
        filtered_chat_list = getchats(self.ut1)
        list_ids = []
        filtered_ids = []
        for lst in list_chats:
            list_ids.append(lst.chat_id)

        for lst in filtered_chat_list:
            filtered_ids.append(lst.chat_id)

        self.assertEqual(list_ids, filtered_ids)

    # controllo invio messaggi
    def test_sendmessage(self):
        mess = Messaggio.objects.filter(chat=self.c, mittente=self.ut1)
        result = mess[0].contenuto
        self.assertEqual(result, "Ciao")
        # invio messaggio ad una chat in cui non si è partecipanti
        result = sendmessage(self.ut1, "Ciao", self.e)
        self.assertEqual(result, "err")

    # controllo contenuto dell'ultimo messaggio inviato
    def test_getlastmessagecontent(self):
        self.assertEqual("Ciao", getlastmessagecontent(self.c))
        self.assertNotEqual("Bye", getlastmessagecontent(self.c))
        # caso in cui non sia stato mandato alcun messaggio
        self.assertEqual("", getlastmessagecontent(self.d))

    # controllo ordine delle chat in base all'orario dell'ultimo messaggio
    def test__getorderedchats(self):
        threads = getorderedchats(self.ut1)
        self.assertEqual(threads[0].chat, self.c)
        sendmessage(self.ut1, "Hey", self.d)
        threads = getorderedchats(self.ut1)
        self.assertNotEqual(threads[0].chat, self.c)
        self.assertEqual(threads[0].chat, self.d)

    # controllo se si tratta di un gruppo o di una chat (restituisce iun utente nel caso sia chat singola)
    def test__getotheruserinchat(self):
        self.assertEqual(getotheruserinchat(self.c, self.ut1), self.ut2)
        self.assertEqual(getotheruserinchat(self.c, self.ut2), self.ut1)
        self.assertNotEqual(getotheruserinchat(self.c, self.ut1), self.ut3)
        self.assertEqual(getotheruserinchat(self.d, self.ut2), "group")
