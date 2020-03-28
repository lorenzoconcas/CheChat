import json
from django.core import exceptions
from django.db.models import Model, QuerySet
from django.http import HttpResponse
from django.shortcuts import render, redirect
from chat.models import *
from chat.utils import *  # importa tutte le funzioni dal file utils.py
from django.template import RequestContext


# Create your views here.
def index(request):
    # questa è la pagina che si presenta all'utente la prima volta che visita il sito se non è loggato
    try:
        logged = request.session['logged']  # vediamo se è loggato
        isdatavalid = request.session['validdata']  # e se i dati inseriti da un ipotetico redirect sono corretti
    except:
        # vuol dire che non vi sono quei dati in sessione, li impostiamo noi
        request.session.__setitem__("logged", False)
        request.session.__setitem__("validdata", True)
        isdatavalid = True
        logged = False

    if logged:
        return redirect("/home")
    else:
        request.session.__setitem__("validdata", True)
        return render(request, 'chat/index.html', {'valid_login': not isdatavalid})


def register(request):
    # questo controllo serve a capire se l'utente ha già inviato i dati per registrarsi (la pagina viene ricaricata
    # alla pressione del tasto registra per verificare i dati
    try:
        registering = request.POST['register']
    except:
        registering = False

    if registering:
        mail = request.POST['mail']
        psw = request.POST['password']
        c_psw = request.POST['confirm_psw']
        name = request.POST['name']
        surname = request.POST['family-name']
        # controlliamo non ci siano campi vuoti
        if mail == "" or psw == "" or name == "" or surname == "":
            return render(request, 'chat/register.html', {
                'response': "Compila tutti i campi",
            })
        # controlliamo la mail non sia già stata usata
        if Utente.objects.filter(email=mail).exists():
            return render(request, 'chat/register.html', {
                'response': "Email già utilizzata",
            })
        # controlliamo le due password coincidano
        if psw != c_psw:
            return render(request, 'chat/register.html', {
                'response': "Le password non corrispondono",
            })
        # avendo superato tutti i controlli aggiungiamo il nuovo utente e lo reindirizziamo al login
        # (si potrebbe fare il login automatico)
        mail = mail.lower()
        new_user = Utente(email=mail, password=psw, nome=name, cognome=surname)
        new_user.save()
        return redirect('/')
    else:
        return render(request, 'chat/register.html')


def home(request):
    # controlliamo che l'utente sia loggato prendendo il valore logged dalla sessione
    try:
        islogged = request.session.get('logged')
    except:  # se il valore non è stato trovato l'utente non è loggato (sessione non valida per esempio)
        islogged = False
        request.session.__setitem__("logged", islogged)
        return redirect('/')  # lo rimandiamo al login

    # la mail è utile per vari scopi quindi cerchiamo di ottenerla anche se non ancora loggato (magari esiste!)
    mail = request.POST.get('mail', '')  # questa funzione cerca l'elemento e se non lo trova resituisce
    if mail is '':  # non vi è una richiesta di login da parte di index
        mail = request.session.get('mail', '')
    if mail is '':  # l'utente non era già loggato in sessione
        return redirect('/')
    # il secondo valore passato
    mail = mail.lower()  # la rendiamo lowercase perchè sono tutte salvate in lowercase per evitare dati incoerenti
    # discorso simile per la psw ma solo per poter tentare il login automatico
    password = request.POST.get('password', '')
    # se non siamo loggati tentiamo il login
    if not islogged:
        # cerchiamo l'utente nel db e se esiste proviamo il login
        if Utente.objects.filter(email=mail).exists():
            u = Utente.objects.get(email=mail)
            if u.login(mail, password):  # se il login riesce segniamo in sessione il flag logged e l'id utente
                request.session.__setitem__("mail", mail)
                request.session.__setitem__("logged", True)
                request.session.__setitem__("user_id", u.id)
            else:  # se non riesce rimandiamo al login, curandoci di settare il flag validdata a seconda del caso per
                # mostrare l'errore solo se davvero necessario
                print("login fallito")
                if mail == '':
                    request.session.__setitem__("validdata", True)
                else:
                    request.session.__setitem__("validdata", False)
                return redirect('/')
        else:  # se l'utente non esiste, come per tutti i casi non validi redirect al login
            if mail == '':
                request.session.__setitem__("validdata", True)
            else:
                request.session.__setitem__("validdata", False)
            return redirect('/')
    # questo gestisce l'immagine del profilo, dovrebbe essere differente per ogni utente ma non verrà implementato
    if mail == 'lore@iswchat.com':
        user_icon = "static/chat/icons/lorec.png"
    else:
        icon_id = int(request.session['user_id'] % 5)
        if icon_id == 0:
            icon_id = 1
        user_icon = 'static/chat/icons/user_icon_' + str(icon_id) + '.png'

    # qui ci occupiamo di caricare tutte le chat dell'utente (quelle nella barra laterale)
    user = Utente.objects.get(email=mail)

    chats = getorderedchats(user)
    # carichiamo i contatti dell'utente, se non esistono elementi restituiamo un array vuoto
    try:
        contacts = Rubrica.objects.filter(owner=user)
    except models.ObjectDoesNotExist:
        contacts = []
    # chiamiamo la pagina passando alcune variabili
    return render(request, 'chat/chats.html', {
        'name_to_show': user.nome + " " + user.cognome,
        'user': user,
        'user_icon': user_icon,
        'chats': chats,
        'contacts': contacts,
    })


def logout(request):
    request.session.flush()
    return redirect("/")


def client_requests(request):
    if request.is_ajax():
        req = request.POST['req']  # otteniamo l'obbiettivo della richiesta
        resp = ""
        user_id = request.session['user_id']
        u = Utente.objects.get(id=user_id)

        if req == 'add_contact':
            email = request.POST['mail']
            try:
                utente = Utente.objects.get(email=email)
            except models.ObjectDoesNotExist:
                resp = '[{"result":"err","error":"Utente non trovato"}]'
                return HttpResponse(resp)

            if u == utente:
                resp = '[{"result":"err","error":"Non si può aggiungere se stessi"}]'
                return HttpResponse(resp)

            if insertcontact(u, utente) == "ok":
                resp = '[{"result":"ok","name":"' + str(utente) + '", "id":"' + str(utente.id) + '"}]'
            else:
                resp = '[{"result":"err","error":"Utente già in rubrica"}]'
        elif req == 'remove_contact':
            try:
                utente = Utente.objects.get(id=request.POST['id'])
                removecontact(u, utente)
            except models.ObjectDoesNotExist:
                print("err")
        elif req == 'create_chat':
            # prendiamo dal json tutti gli id degli utenti da aggiungere alla chat
            ids_json = json.loads(request.POST['user_ids_json'])
            ids = []
            for e in ids_json:
                ids.append(int(e))

            adding_to_thread = request.POST['starting_thread']
            print(adding_to_thread)
            if adding_to_thread is not None and adding_to_thread == 'true':
                # significa che l'utente ha creato una chat
                # aggiungendo dei partecipanti e dobbiamo essere sicuri
                # che l'id dell'altro utente non sia già selezionato
                thread_id = request.POST['base_thread']
                if not thread_id == 0:
                    try:
                        chat = Chat.objects.get(id=thread_id)
                        partecipanti = Partecipanti.objects.filter(chat=chat).exclude(contatto=u)
                        if len(partecipanti) == 1:  # se ci sono due partecipanti è una chat singola
                            altro_partecipante = partecipanti[0]
                            other_user = altro_partecipante.contatto
                            if int(other_user.id) not in ids:
                                ids.append(int(other_user.id))
                        elif len(partecipanti) > 1:  # altrimenti è un gruppo, quindi esiste
                            for partecipante in partecipanti:
                                if not Partecipanti.objects.filter(chat=chat, contatto=partecipante.contatto).exists():
                                    addusertochat(chat, partecipante.contatto)
                            return HttpResponse('[{"result":"ok", "id":"' + str(chat.id) + '" }]')
                    except exceptions.ObjectDoesNotExist:
                        print("L'utente sta cercando di aggiungere un partecipante ad una conversazione che non esiste")
            c = createchat(u, ids)
            resp = '[{"result":"ok","id":"' + str(c.id) + '"}]'
        elif req == 'delete_chat':
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
            # controlliamo che l'utente sia effettivamente in quella chat
            if Partecipanti.objects.filter(chat=chat, contatto=u).exists():
                messaggi = Messaggio.objects.filter(chat_id=chat_id)
                resp = "["
                # trasformiamo i messaggi in una linea json e la aggiungiamo alla risposta
                for m in messaggi:
                    if m.mittente_id == user_id:
                        resp = resp + json_element(m.dataora, m.contenuto, True, "") + ","
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
            c = Chat.objects.get(id=chat_id)
            if Partecipanti.objects.filter(chat=c, contatto=u).exists():
                sendmessage(u, msg, c)
                resp = "sent"
            else:
                resp = "non allowed"
        elif req == 'search_chats':
            resp = ''
        elif req == 'get_chat_icon':
            chat_id = request.POST['chat_id']
            chat = getchat(chat_id)
            if chat == "":
                resp = ""
            else:
                other_user = getotheruserinchat(chat, u)
                if other_user == "":
                    resp = 'static/chat/icons/user_icon_1.png'
                elif other_user == "group":
                    resp = 'static/chat/icons/user_group.png'
                else:
                    other_id = other_user.id
                    img_id = int(other_id) % 5

                    if img_id == 0:
                        img_id = 1
                    resp = 'static/chat/icons/user_icon_' + str(img_id) + '.png'

        return HttpResponse(resp)
    else:
        return redirect("/")
