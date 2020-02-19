from django.db import models
from datetime import datetime, timezone


# Create your models here.
class Utente(models.Model):
    nome = models.CharField(max_length=200)
    cognome = models.CharField(max_length=200)
    email = models.CharField(max_length=200)
    password = models.CharField(max_length=200)

    def __str__(self):
        return "User call himself : " + self.nome

    def login(self, mail, password):
        return (self.email == mail) and (self.password == password)


class Rubrica(models.Model):
    owner = models.ForeignKey(to=Utente, on_delete=models.CASCADE)
    contatto = models.IntegerField


class Chat(models.Model):
    creatore = models.ForeignKey(to=Utente, on_delete=models.CASCADE)
    nome = models.CharField(max_length=200)


class Partecipanti(models.Model):  # i partcipanti di una chat
    chat = models.ForeignKey(to=Chat, on_delete=models.CASCADE)
    contatto = models.ForeignKey(to=Utente, on_delete=models.CASCADE)


def sendmessage(utente, messaggio, chat):
    m = Messaggio(mittente=utente, contenuto=messaggio, chat=chat, dataora=datetime.utcnow())
    m.save()


def getlastmessagecontent(chat):
    msg_list = Messaggio.objects.filter(chat=chat)
    try:
        return msg_list.latest('dataora').contenuto
    except:
        return ""


def getlastmessage(chat):
    msg_list = Messaggio.objects.filter(chat=chat)
    try:
        return msg_list.latest('dataora')
    except:
        return ""


class Messaggio(models.Model):
    chat = models.ForeignKey(to=Chat, on_delete=models.CASCADE)
    mittente = models.ForeignKey(to=Utente, on_delete=models.CASCADE)
    dataora = models.DateTimeField()
    contenuto = models.CharField(max_length=2000)

