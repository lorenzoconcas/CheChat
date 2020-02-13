from django.http import HttpResponse
from django.shortcuts import render
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
    ip = get_client_ip(request)
    print(ip)
    with open("index.txt", "a+") as myfile:
        myfile.write(ip)
        myfile.write("\t")
        myfile.write(datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
        myfile.write(" \n")
    return render(request, 'chat/index.html')


def register(request):
    return render(request, 'chat/register.html')


def home(request):
    test = "static/chat/icons/"
    mail = request.POST.get('mail', 'lore@iswchat.com')
    if mail == 'lore@iswchat.com':
        user_icon = "lorec.png"
    else:
        user_icon = "generic_user.png"
    final_icon = test + user_icon
    print(final_icon)
    return render(request, 'chat/chats.html', {'name_to_show': mail, 'user_icon': final_icon})
