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


@register.filter(name='cut')
def cutmsg(msg, arg):
    count = int(arg)
    if msg.__len__() > count:
        return msg[:count] + '...'
    else:
        return msg


@register.filter(name='fontsize')
def fontsize(msg, args):
    arg_list = [arg.strip() for arg in args.split(',')]
    count = int(arg_list[1])
    if msg.__len__() > count:
        return "font-size:"+str(arg_list[2])+"px"
    else:
        return ""


@register.filter()
def sentbyuser(messaggio, utente):
    if messaggio.mittente == utente:
        return "outgoing"
    else:
        return "incoming"

