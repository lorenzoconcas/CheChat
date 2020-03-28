from django import template
from chat.models import *


register = template.Library()


# serve ad ottenere l'ultimo messaggio di una chat e tagliarlo dopo un certo tot di caratteri
# viene usato nel template per non caricare troppo la view di calcoli (con un for andrebbe ripulito l'array thread
# e non sarebbe dinamico a seconda della dimensione del messaggio
@register.filter(name='getltsmsg')
def getltsmsg(partecipanti):
    response = getlastmessagecontent(partecipanti.chat)
    return response
