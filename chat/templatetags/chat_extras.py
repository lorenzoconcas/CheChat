from django import template
from chat.models import *


register = template.Library()


@register.filter(name='getltsmsg')
def getltsmsg(partecipanti, arg):
    count = int(arg)
    response = getlastmessagecontent(partecipanti.chat)
    if response.__len__() > count:
        return response[:count] + '...'
    else:
        return response


@register.filter()
def sentbyuser(messaggio, utente):
    if messaggio.mittente == utente:
        return "outgoing"
    else:
        return "incoming"

