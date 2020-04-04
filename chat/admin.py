from django.contrib import admin
from chat.models import *
# Register your models here.

admin.site.register(Utente)
admin.site.register(Chat)
admin.site.register(Partecipanti)
admin.site.register(Messaggio)
admin.site.register(Rubrica)
