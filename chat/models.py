from django.db import models


# Create your models here.
class Utente(models.Model):
    nome = models.CharField(max_length=200)
    cognome = models.CharField(max_length=200)
    email = models.CharField(max_length=200)
    password = models.CharField(max_length=200)


class ListaContatti(models.Model):
    utente = models.ForeignKey(to=Utente, on_delete=models.CASCADE())


class Rubrica(models.Model):
    utente = models.ForeignKey(to=Utente, on_delete=models.CASCADE())
    listaContatti = models.ForeignKey(to=ListaContatti, on_delete=models.CASCADE())


class Messaggio(models.Model):
    mittente = models.ForeignKey(to=Utente, on_delete=models.CASCADE())
    dataora = models.DateTimeField()
    contenuto = models.CharField(max_length=2000)


class ListaMessaggi(models.Model):
    idMessaggio = models.ForeignKey(to=Messaggio, on_delete=models.CASCADE())


class Chat(models.Model):
    creatore = models.ForeignKey(to=Utente, on_delete=models.CASCADE())
    nome = models.CharField(max_length=200)
    partecipanti = models.ForeignKey(to=ListaContatti, on_delete=models.CASCADE())
    messaggi = models.ForeignKey(to=ListaMessaggi, on_delete=models.CASCADE())
