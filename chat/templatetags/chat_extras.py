from django import template
from chat.models import *


register = template.Library()


# serve ad ottenere l'ultimo messaggio di una chat e tagliarlo dopo un certo tot di caratteri
# viene usato nel template per non caricare troppo la view di calcoli (con un for andrebbe ripulito l'array thread
# e non sarebbe dinamico a seconda della dimensione del messaggio
@register.filter(name='getltsmsg')
def getltsmsg(partecipanti, arg):
    count = int(arg)
    response = getlastmessagecontent(partecipanti.chat)
    if len(response) > count:
        return response[:count] + '...'
    else:
        return response


# taglia un messaggio dopo un certo numero di caratteri
# discorso simile a quello precedente
@register.filter(name='cut')
def cutmsg(msg, arg):
    count = int(arg)
    if len(msg) > count:
        return msg[:count] + '...'
    else:
        return msg
