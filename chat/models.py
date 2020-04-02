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
        return "Contatto : " + str(self.contatto) + ", nella rubrica di " + str(self.owner)


class Chat(models.Model):
    creatore = models.ForeignKey(to=Utente, on_delete=models.CASCADE)
    nome = models.CharField(max_length=200)

    def __str__(self):
        return self.nome + ",  creata da " + str(self.creatore)


class Partecipanti(models.Model):  # i partecipanti di una chat
    chat = models.ForeignKey(to=Chat, on_delete=models.CASCADE)
    contatto = models.ForeignKey(to=Utente, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Partecipanti'
        verbose_name_plural = 'Partecipanti'

    def __str__(self):
        return str(self.contatto) + " partecipa nella chat " + \
               self.chat.nome.replace(self.contatto.nome + " " + self.contatto.cognome, "")


class Messaggio(models.Model):
    chat = models.ForeignKey(to=Chat, on_delete=models.CASCADE)
    mittente = models.ForeignKey(to=Utente, on_delete=models.CASCADE)
    dataora = models.DateTimeField()
    contenuto = models.CharField(max_length=2000)

    def __str__(self):
        return str(self.mittente) + " dice : " + self.contenuto + ", nella chat : " + self.chat.nome

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
        chat_name = chat_name + str(utente)

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
        p = Partecipanti.objects.filter(chat=target_chat, contatto=user)  # togliamo l'accesso alla chat all'utente
        # print(len(p))
        p[0].delete()  # perchè [0] ? filter restituisce un queryset non un entry singola,
        # anche se restituirà un solo elemento
    except models.ObjectDoesNotExist:
        print("L'utente sta cercando di cancellarsi da una chat non sua o non esiste in quella chat")
    if len(users_in_chat) == 0:  # se anche l'ultimo partecipante è stato cancellato eliminiamo la chat
        target_chat.delete()


def addusertochat(chat, user):
    Partecipanti(chat=chat, contatto=user).save()


def getchat(chat_id):
    try:
        c = Chat.objects.get(id=chat_id)
        return c
    except models.ObjectDoesNotExist:
        return ""


# restituisce le chat a cui partecipa l'utente (già col nome filtrato)
def getchats(user):
    threads = Partecipanti.objects.filter(contatto=user)
    for t in threads:
        if not t.chat.nome.startswith("Gruppo"):
            t.chat.nome = t.chat.nome.replace(user.nome + " " + user.cognome, "")
    return threads


def getorderedchats(user):
    threads = []
    for t in Partecipanti.objects.filter(contatto=user).order_by('chat__messaggio__dataora').reverse():
        if t not in threads:
            threads.append(t)

    for t in threads:
        if not t.chat.nome.startswith("Gruppo"):
            t.chat.nome = t.chat.nome.replace(user.nome + " " + user.cognome, "")

    return threads


def getuser(user_id):
    try:
        u = Utente.objects.get(id=user_id)
        return u
    except models.ObjectDoesNotExist:
        return ""


def getotheruserinchat(chat, current_user):
    try:
        u = Partecipanti.objects.filter(chat=chat).exclude(contatto=current_user)
        if len(u) > 1:
            return "group"
        else:
            return u[0].contatto
    except models.ObjectDoesNotExist:
        return ""
