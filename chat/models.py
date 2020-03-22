from django.db import models
from datetime import datetime
from chat.utils import *


class Utente(models.Model):
    nome = models.CharField(max_length=200)
    cognome = models.CharField(max_length=200)
    email = models.CharField(max_length=200)
    password = models.CharField(max_length=200)

    def __str__(self):
        return self.nome + " " + self.cognome

    def login(self, mail, password):
        return (self.email == mail) and (self.password == password)

    class Meta:
        verbose_name = 'Utente'
        verbose_name_plural = 'Utenti'


class Rubrica(models.Model):
    owner = models.ForeignKey(to=Utente, on_delete=models.CASCADE, related_name='owner')
    contatto = models.ForeignKey(to=Utente, on_delete=models.CASCADE, related_name='contact')

    class Meta:
        verbose_name = 'Rubrica'
        verbose_name_plural = 'Rubriche'

    def __str__(self):
        return "Contatto : " + self.contatto.__str__() + ", nella rubrica di " + self.owner.__str__()


class Chat(models.Model):
    creatore = models.ForeignKey(to=Utente, on_delete=models.CASCADE)
    nome = models.CharField(max_length=200)

    def __str__(self):
        return self.nome + ",  creata da " + self.creatore.__str__()


class Partecipanti(models.Model):  # i partcipanti di una chat
    chat = models.ForeignKey(to=Chat, on_delete=models.CASCADE)
    contatto = models.ForeignKey(to=Utente, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Partecipanti'
        verbose_name_plural = 'Partecipanti'

    def __str__(self):
        return self.contatto.__str__() + " partecipa nella chat " + \
               self.chat.nome.replace(self.contatto.nome+" "+self.contatto.cognome, "").replace("-&/&-", "")


class Messaggio(models.Model):
    chat = models.ForeignKey(to=Chat, on_delete=models.CASCADE)
    mittente = models.ForeignKey(to=Utente, on_delete=models.CASCADE)
    dataora = models.DateTimeField()
    contenuto = models.CharField(max_length=2000)

    def __str__(self):
        return self.mittente.__str__() + " dice : " + self.contenuto + ", nella chat : " + self.chat.nome

    class Meta:
        verbose_name = 'Messaggio'
        verbose_name_plural = 'Messaggi'


# funzioni di supporto per le tabelle

def insertcontact(phonebook_owner, contact):
    if Rubrica.objects.filter(owner=phonebook_owner, contatto=contact).exists():
        return "exists"
    else:
        phonebook_element = Rubrica(owner=phonebook_owner, contatto=contact)
        phonebook_element.save()
        return "ok"


def removecontact(phonebook_owner, contact):
    try:
        Rubrica.objects.get(owner=phonebook_owner, contatto=contact).delete()
    except models.ObjectDoesNotExist:
        print("contatto non trovato in rubrica")


def createchat(utente, id_utenti):
    if len(id_utenti) == 1:
        altro_u = Utente.objects.get(id=id_utenti[0])
        chat_name = str(utente) + " " + str(altro_u)
    else:
        chat_name = "Gruppo : "
        for i in id_utenti:
            chat_name = chat_name + str(Utente.objects.get(id=i)) + ", "
        chat_name = chat_name + utente.__str__()

    c = Chat(creatore=utente, nome=chat_name)
    c.save()
    p = Partecipanti(chat=c, contatto=utente)
    p.save()
    for i in id_utenti:
        u = Utente.objects.get(id=i)
        p = Partecipanti(chat=c, contatto=u)
        p.save()

    return c


def sendmessage(utente, messaggio, chat):
    m = Messaggio(mittente=utente, contenuto=messaggio, chat=chat, dataora=datetime.utcnow())
    m.save()


def getlastmessagecontent(chat):
    msg_list = Messaggio.objects.filter(chat=chat)

    try:
        return msg_list.latest('dataora').contenuto
    except models.ObjectDoesNotExist:
        return ""


def getlastmessage(chat):
    msg_list = Messaggio.objects.filter(chat=chat)
    try:
        return msg_list.latest('dataora')
    except models.ObjectDoesNotExist:
        return ""


def deletechat(user_id, chat_id):
    user = Utente.objects.get(id=user_id)
    target_chat = Chat.objects.get(id=chat_id)
    users_in_chat = Partecipanti.objects.filter(chat=target_chat)  # restituisce tutti i partecipanti ad una chat
    try:
        Partecipanti.objects.get(chat=target_chat, contatto=user).delete()  # togliamo l'accesso alla chat all'utente
    except models.ObjectDoesNotExist:
        print("L'utente sta cercando di cancellarsi da una chat non sua o non esiste in quella chat")
    if len(users_in_chat) == 0:  # se anche l'ultimo partecipante è stato cancellato eliminiamo la chat
        target_chat.delete()
