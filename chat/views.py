import json
from django.core import exceptions
from django.db.models import Model
from django.http import HttpResponse
from django.shortcuts import render, redirect
from chat.models import *
from chat.utils import *  # importa tutte le funzioni dal file utils.py


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
    # ip = get_client_ip(request)
    # print(ip)
    # if not ip.startswith('192.168'):
    #     with open("index.txt", "a+") as myfile:
    #         myfile.write(ip)
    #         myfile.write("\t")
    #         myfile.write(datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
    #         myfile.write(" \n")

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


def home(request):
    test = "static/chat/icons/"
    try:
        #  islogged = request.session.__getitem__("logged")
        islogged = request.session['logged']
    except:
        islogged = False
        request.session.__setitem__("logged", islogged)
        return redirect('/')

    try:
        mail = request.session['mail']
    except:
        mail = request.POST.get('mail', '')
        mail = mail.lower()

    try:
        password = request['password']
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
        user_icon = "static/chat/icons/lorec.png"
    else:
        user_icon = "static/chat/icons/generic_user.png"

    user = Utente.objects.get(email=mail)
    request.session.__setitem__("user_id", user.id)
    threads = Partecipanti.objects.filter(contatto=user)

    for t in threads:
        if not t.chat.nome.startswith("Gruppo"):
            t.chat.nome = t.chat.nome.replace(user.nome + " " + user.cognome, "")

    try:
        contacts = Rubrica.objects.filter(owner=user)
    except:
        contacts = []

    return render(request, 'chat/chats.html', {
        'name_to_show': user.nome + " " + user.cognome,
        'user': user,
        'user_icon': user_icon,
        'Threads': threads,
        'contacts': contacts,
    })


def logout(request):
    request.session.flush()
    return redirect("/")


def test(request):
    return render(request, "chat/test.html")


def client_requests(request):
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
                removecontact(u, utente)
            except:
                print("err")
        elif req == 'create_chat':
            ids_json = json.loads(request.POST['user_ids_json'])
            ids = []
            for e in ids_json:
                print(e)
                ids.append(int(e))
            c = createchat(u, ids)
            resp = '[{"result":"ok","id":"' + str(c.id) + '","name":"' + c.nome.replace(str(u), ""). \
                replace("-&/&-", "") + '"}]'
        elif req == 'delete_chat':
            print("User request deletion of chat "+request.POST['chat_id'])
            deletechat(user_id, request.POST['chat_id'])
            resp = '[{"delete":"ok"}]'
        elif req == 'personal_id':
            resp = request.session['user_id']
        elif req == 'get_all_messages':  # restituisce tutti i messaggi di una data conversazione
            chat_id = request.POST["chat_id"]
            try:
                chat = Chat.objects.get(id=chat_id)
            except exceptions.ObjectDoesNotExist:
                print("la chat non esiste")
                return HttpResponse("[]")
            print(chat)
            # controlliamo che l'utente sia effettivamente in quella chat
            if Partecipanti.objects.filter(chat=chat, contatto=u).exists():
                messaggi = Messaggio.objects.filter(chat_id=chat_id)
                resp = "["
                # trasformiamo i messaggi in una linea json e la aggiungiamo alla risposta
                for m in messaggi:
                    if m.mittente_id == user_id:
                        resp = resp + json_element(m.dataora, m.contenuto, True, (m.mittente.nome + " " +
                                                                                  m.mittente.cognome)) + ","
                    else:
                        resp = resp + json_element(m.dataora, m.contenuto, False, (m.mittente.nome + " " +
                                                                                   m.mittente.cognome)) + ","
                resp = resp[:-1]
                resp += "]"
            else:
                print("l'utente non ha accesso alla chat")
                resp = "[]"
        elif req == 'send_message':
            msg = request.POST['msg']
            chat_id = request.POST['chat_id']
            u = Utente.objects.get(id=user_id)
            c = Chat.objects.get(id=chat_id)
            sendmessage(u, msg, c)
            resp = "sent"

        return HttpResponse(resp)
    else:
        return redirect("/")
