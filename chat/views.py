from django.http import HttpResponse
from django.shortcuts import render, redirect
from datetime import datetime
from chat.models import *


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


# Create your views here.
def index(request):
    try:
        logged = request.session.__getitem__("logged")
        isdatavalid = request.session.__getitem__("validdata")
    except:
        # vuol dire che non vi sono quei dati in sessione, li impostiamo noi
        request.session.__setitem__("logged", False)
        request.session.__setitem__("validdata", True)
        isdatavalid = True  # se non ci sono significa che
        logged = False

    print(isdatavalid)
    ip = get_client_ip(request)
    print(ip)
    if not ip.startswith('192.168'):
        with open("index.txt", "a+") as myfile:
            myfile.write(ip)
            myfile.write("\t")
            myfile.write(datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
            myfile.write(" \n")

    if logged:
        return redirect("/home")
    else:
        request.session.__setitem__("validdata", True)
        return render(request, 'chat/index.html', {'valid_login': not isdatavalid})


def register(request):
    return render(request, 'chat/register.html')


def home(request):
    test = "static/chat/icons/"
    try:
        islogged = request.session.__getitem__("logged")
    except:
        islogged = False
        request.session.__setitem__("logged", islogged)
        return redirect('/')


    try:
        mail = request.session.__getitem__("mail")
    except:
        mail = request.POST.get('mail', '')
    try:
        password = request.session.__getitem__("password")
    except:
        password = request.POST.get('password', '')

    if not islogged:
        u = Utente.objects.filter(email=mail)

        if u.exists():
            u = Utente.objects.get(email=mail)
            if u.login(mail, password):
                request.session.__setitem__("mail", mail)
                request.session.__setitem__("logged", True)
            else:
                if mail == '':
                    request.session.__setitem__("validdata", True)
                else:
                    request.session.__setitem__("validdata", False)
                return redirect('/')
        else:
            if mail == '':
                request.session.__setitem__("validdata", True)
            else:
                request.session.__setitem__("validdata", False)
            return redirect('/')

    if mail == 'lore@iswchat.com':
        user_icon = "lorec.png"
    else:
        user_icon = "generic_user.png"

    final_icon = test + user_icon
    user = Utente.objects.get(email=mail)
    threads = Partecipanti.objects.filter(contatto=user)
    for t in threads:
        t.chat.nome = t.chat.nome.replace(user.nome+" "+user.cognome+"-&/&-", "")

    messages = Messaggio.objects.filter(chat_id=1)
    return render(request, 'chat/chats.html', {
                    'name_to_show': user.nome+" "+user.cognome,
                    'user': user,
                    'user_icon': final_icon,
                    'Threads': threads,
                    'messages': messages
                   })


def logout(request):
    request.session.flush()
    return redirect("/")


def test(request):
    rText = ""
    for messaggio in Messaggio.objects.all():
        rText = rText + messaggio.contenuto + " spedito da " + messaggio.mittente.nome + " nella chat : "+ messaggio.chat.nome +"<br>"

    io = Utente.objects.get(id=1)
    for partecipanti in Partecipanti.objects.filter(contatto=io):
        rText = rText + partecipanti.chat.nome + " a cui partecipa "+partecipanti.contatto.nome + "<br>"

    return HttpResponse(rText)