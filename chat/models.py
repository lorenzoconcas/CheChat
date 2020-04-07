from django.db import models
from datetime import datetime
from chat.utils import *


class Users(models.Model):
    name = models.CharField(max_length=200)
    surname = models.CharField(max_length=200)
    email = models.CharField(max_length=200)
    password = models.CharField(max_length=200)

    def __str__(self):
        return self.name + " " + self.surname

    def login(self, mail, password):
        return (self.email == mail) and (self.password == password)

    class Meta:
        verbose_name = 'Users'
        verbose_name_plural = 'Utenti'


class Phonebook(models.Model):
    owner = models.ForeignKey(to=Users, on_delete=models.CASCADE, related_name='owner')
    contact = models.ForeignKey(to=Users, on_delete=models.CASCADE, related_name='contact')

    class Meta:
        verbose_name = 'Phonebook'
        verbose_name_plural = 'Rubriche'

    def __str__(self):
        return "Contatto: " + str(self.contact) + ", nella rubrica di " + str(self.owner)


class Chat(models.Model):
    creator = models.ForeignKey(to=Users, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name + ",  creata da " + str(self.creator)


class Partecipants(models.Model):  # i partecipanti di una chat
    chat = models.ForeignKey(to=Chat, on_delete=models.CASCADE)
    contact = models.ForeignKey(to=Users, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Partecipants'
        verbose_name_plural = 'Partecipants'

    def __str__(self):
        return str(self.contact) + " partecipa nella chat " + \
               self.chat.name.replace(self.contact.name + " " + self.contact.surname, "")


class Messages(models.Model):
    chat = models.ForeignKey(to=Chat, on_delete=models.CASCADE)
    sender = models.ForeignKey(to=Users, on_delete=models.CASCADE)
    time = models.DateTimeField()
    content = models.CharField(max_length=2000)

    def __str__(self):
        return str(self.sender) + " dice: " + self.content + ", nella chat: " + self.chat.name

    class Meta:
        verbose_name = 'Messages'
        verbose_name_plural = 'Messaggi'


# funzioni di supporto per le tabelle

def insertcontact(phonebook_owner, contact):
    if Phonebook.objects.filter(owner=phonebook_owner, contact=contact).exists():
        return "exists"
    else:
        phonebook_element = Phonebook(owner=phonebook_owner, contact=contact)
        phonebook_element.save()
        return "ok"


def removecontact(phonebook_owner, contact):
    try:
        Phonebook.objects.get(owner=phonebook_owner, contact=contact).delete()
        return "ok"
    except models.ObjectDoesNotExist:
        # print("contact non trovato in rubrica")
        return "err"


def createchat(utente, id_utenti):
    if len(id_utenti) == 1:
        altro_u = Users.objects.get(id=id_utenti[0])
        chat_name = str(utente) + " " + str(altro_u)
    else:
        chat_name = "Gruppo: "
        for i in id_utenti:
            chat_name = chat_name + str(Users.objects.get(id=i)) + ", "
        chat_name = chat_name + str(utente)

    c = Chat(creator=utente, name=chat_name)
    c.save()
    p = Partecipants(chat=c, contact=utente)
    p.save()
    for i in id_utenti:
        u = Users.objects.get(id=i)
        p = Partecipants(chat=c, contact=u)
        p.save()

    return c


def sendmessage(utente, messaggio, chat):
    if not Partecipants.objects.filter(chat=chat, contact=utente).exists():
        return "err"
    m = Messages(sender=utente, content=messaggio, chat=chat, time=datetime.utcnow())
    m.save()


def getlastmessagecontent(chat):
    msg_list = Messages.objects.filter(chat=chat)
    try:
        return msg_list.latest('time').content
    except models.ObjectDoesNotExist:
        return ""


def deletechat(user_id, chat_id):
    user = Users.objects.get(id=user_id)
    try:
        target_chat = Chat.objects.get(id=chat_id)
    except models.ObjectDoesNotExist:
        return "err"
    users_in_chat = Partecipants.objects.filter(chat=target_chat)  # restituisce tutti i partecipanti ad una chat
    try:
        p = Partecipants.objects.filter(chat=target_chat, contact=user)  # togliamo l'accesso alla chat all'utente
        # print(len(p))
        p[0].delete()  # perchè [0] ? filter restituisce un queryset non un entry singola,
        # anche se restituirà un solo elemento
    except (models.ObjectDoesNotExist, IndexError):
        # print("L'utente sta cercando di cancellarsi da una chat non sua o non esiste in quella chat")
        return "err"

    if len(users_in_chat) == 0:  # se anche l'ultimo partecipante è stato cancellato eliminiamo la chat
        target_chat.delete()

    return "ok"


def addusertochat(chat, user):
    if not Partecipants.objects.filter(chat=chat, contact=user).exists():
        Partecipants(chat=chat, contact=user).save()
    else:
        return "err"


def getchat(chat_id):
    try:
        c = Chat.objects.get(id=chat_id)
        return c
    except models.ObjectDoesNotExist:
        return ""


# restituisce le chat a cui partecipa l'utente (già col nome filtrato)
def getchats(user):
    threads = Partecipants.objects.filter(contact=user)
    for t in threads:
        if not t.chat.name.startswith("Gruppo"):
            # proviamo a togliere il nome se con la virgola e poi senza
            t.chat.name = t.chat.name.replace(user.name + " " + user.surname + " ,", "")
            t.chat.name = t.chat.name.replace(user.name + " " + user.surname, "")
    return threads


def getorderedchats(user):
    threads = []
    for t in Partecipants.objects.filter(contact=user).order_by('chat__messages__time').reverse():
        if t not in threads:
            threads.append(t)

    for t in threads:
        if not t.chat.name.startswith("Gruppo"):
            t.chat.name = t.chat.name.replace(user.name + " " + user.surname, "")

    return threads


def getuser(user_id):
    try:
        u = Users.objects.get(id=user_id)
        return u
    except models.ObjectDoesNotExist:
        return ""


def getotheruserinchat(chat, current_user):
    try:
        u = Partecipants.objects.filter(chat=chat).exclude(contact=current_user)
        u_len = len(u)
        if u_len == 1:
            u_1 = u[0].contact
            if u_1 is None:
                return ""
            return u_1
        elif u_len > 1:
            return "group"
        else:
            return ""
    except models.ObjectDoesNotExist:
        return ""
