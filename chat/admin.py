from django.contrib import admin

# Register your models here.

from chat.models import *

admin.site.register(Utente)
admin.site.register(Chat)
admin.site.register(Partecipanti)
admin.site.register(Messaggio)
admin.site.register(Rubrica)
