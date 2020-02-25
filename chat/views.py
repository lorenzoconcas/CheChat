import json

from django.http import HttpResponse
from django.shortcuts import render, redirect
from chat.models import *
import asyncio
from channels.consumer import AsyncConsumer


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
    try:
        registering = request.POST['register']
    except:
        registering = False
    print(registering)
    if registering:
        mail = request.POST['mail']
        psw = request.POST['password']
        c_psw = request.POST['confirm_psw']
        name = request.POST['name']
        surname = request.POST['family-name']

        if mail == "" or psw == "" or name == "" or surname == "":
            return render(request, 'chat/register.html', {
                'response': "Compila tutti i campi",
            })

        if Utente.objects.filter(email=mail).exists():
            return render(request, 'chat/register.html', {
                'response': "Email già utilizzata",
            })

        if psw != c_psw:
            return render(request, 'chat/register.html', {
                'response': "Le password non corrispondono",
            })
        mail = mail.lower()
        new_user = Utente(email=mail, password=psw, nome=name, cognome=surname)
        new_user.save()
        return redirect('/')

    else:
        return render(request, 'chat/register.html')


def info(request):
    if request.is_ajax():
        msg = request.POST['msg']
        print(msg)
        if msg == 'personal_id':
            resp = HttpResponse(request.session['user_id'])
            print(resp)
            return resp
        else:
            return HttpResponse("")
    else:
        return HttpResponse("")


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
        mail = mail.lower()

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
                request.session.__setitem__("user_id", u.id)
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
    request.session.__setitem__("user_id", user.id)
    threads = Partecipanti.objects.filter(contatto=user)

    for t in threads:
        if not t.chat.nome.startswith("Gruppo"):
            t.chat.nome = t.chat.nome.replace(user.nome + " " + user.cognome, "").replace("-&/&-", "")

    try:
        contacts = Rubrica.objects.filter(owner=user)
    except:
        contacts = []

    return render(request, 'chat/chats.html', {
        'name_to_show': user.nome + " " + user.cognome,
        'user': user,
        'user_icon': final_icon,
        'Threads': threads,
        'contacts': contacts,
    })


def logout(request):
    request.session.flush()
    return redirect("/")


def test(request):
    return render(request, "chat/test.html")


def snmsg(request):
    if request.is_ajax():
        msg = request.POST['msg']
        user_id = request.session['user_id']
        chat_id = request.POST['chat_id']
        u = Utente.objects.get(id=user_id)
        c = Chat.objects.get(id=chat_id)
        sendmessage(u, msg, c)
        return HttpResponse("sent")
    else:
        return redirect("/")


def send_data(request):
    if request.is_ajax():
        req = request.POST['req']
        resp = ""
        user_id = request.session['user_id']
        u = Utente.objects.get(id=user_id)

        if req == 'add_contact':
            email = request.POST['mail']
            try:
                utente = Utente.objects.get(email=email)
            except:
                resp = '[{"result":"err","error":"Utente non trovato"}]'
                return HttpResponse(resp)

            if u == utente:
                resp = '[{"result":"err","error":"Non si può aggiungere se stessi"}]'
                return HttpResponse(resp)

            if insertcontact(u, utente) == "ok":
                resp = '[{"result":"ok","name":"' + utente.__str__() + '", "id":"' + str(utente.id) + '"}]'
            else:
                resp = '[{"result":"err","error":"Utente già in rubrica"}]'
        elif req == 'remove_contact':

            id = request.POST['id']
            try:
                utente = Utente.objects.get(id=id)
                remove_contact(u, utente)
            except:
                print("err")
        elif req == 'create_chat':
            ids_json = json.loads(request.POST['user_ids_json'])
            ids = []

            for e in ids_json:
                print(e)
                ids.append(int(e))

            c = createchat(u, ids)

            resp = '[{"result":"ok","id":"' + str(c.id) + '","name":"' + c.nome.replace(str(u), "").\
                replace("-&/&-", "") + '"}]'
        return HttpResponse(resp)
    else:
        return redirect("/")


def lstmsg(request):
    if request.is_ajax():
        user_id = request.session['user_id']
        u = Utente.objects.get(id=user_id)
        chat_id = request.POST['chat_id']
        c = Chat.objects.get(id=chat_id)

        msg = getlastmessage(c)

        try:
            sent = msg.mittente == u
        except:
            sent = False

        if not sent:
            response = "[" + getJSONLine(dataora=msg.dataora, contenuto=msg.contenuto, sent=sent,
                                         mittente=(msg.mittente.nome + " " + msg.mittente.cognome)) + "]"
        else:
            response = ""
        return HttpResponse(response)

    else:
        return HttpResponse("")


def getJSONLine(dataora, contenuto, sent, mittente):
    return '{"dataora":"' + dataora.strftime("%Y-%m-%d %H:%M:%S") + '", "contenuto":"' \
           + contenuto + '", "inviato":"' + str(sent) + '", "mittente":"' + mittente + '"}'


class MyJsonEncoder:
    def default(self, obj):
        if isinstance(obj, JSONMsg):
            return {}  # dict representation of your object
        return super(MyJsonEncoder, self).dumps(obj)


def allmsg(request):
    if request.is_ajax():
        chat_id = request.POST["chat_id"]
        user_id = request.session['user_id']
        messaggi = Messaggio.objects.filter(chat_id=chat_id)
        msg = []
        for m in messaggi:
            if m.mittente_id == user_id:
                msg.append(JSONMsg(m.dataora, m.contenuto, True, ""))
            else:
                msg.append(JSONMsg(m.dataora, m.contenuto, False, m.mittente.nome + " " + m.mittente.cognome))
        json_response = "["
        for x in msg:
            json_response = json_response + getJSONLine(x.ora, x.contenuto, x.inviato, x.mittente) + ","

        json_response += "]"
        return HttpResponse(json_response.replace(",]", "]"))

    return redirect("/")


class JSONMsg(object):
    ora = datetime.now()
    contenuto = ""
    inviato = True
    mittente = ""

    # The class "constructor" - It's actually an initializer
    def __init__(self, ora, contenuto, inviato, mittente):
        self.ora = ora
        self.contenuto = contenuto
        self.inviato = inviato
        self.mittente = mittente
