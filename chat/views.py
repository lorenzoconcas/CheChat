from django.http import HttpResponse
from django.shortcuts import render


# Create your views here.
def index(request):
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
