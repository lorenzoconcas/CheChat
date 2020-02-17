from django.shortcuts import render, redirect
from datetime import datetime


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
    islogged = request.session.__getitem__("logged")
    maillist = ["lore@iswchat.com", "test@iswchat.com"]
    try:
        mail = request.session.__getitem__("mail")
    except:
        mail = request.POST.get('mail', 'lore@iswchat.com')

    if not islogged:

        if mail not in maillist:
            request.session.__setitem__("validdata", False)
            return redirect('/')
        else:
            request.session.__setitem__("mail", mail)
            request.session.__setitem__("logged", True)

    if mail == 'lore@iswchat.com':
        user_icon = "lorec.png"
    else:
        user_icon = "generic_user.png"

    final_icon = test + user_icon
    return render(request, 'chat/chats.html', {'name_to_show': mail, 'user_icon': final_icon})


def logout(request):
    request.session.flush()
    return redirect("/")
