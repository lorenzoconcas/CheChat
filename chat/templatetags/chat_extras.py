from django import template
from chat.models import *


register = template.Library()


@register.filter(name='getltsmsg')
def getltsmsg(partecipanti):
    return getlastmessagecontent(partecipanti.chat)


@register.filter()
def sentbyuser(messaggio, utente):
    if messaggio.mittente == utente:
        return "outgoing"
    else:
        return "incoming"

