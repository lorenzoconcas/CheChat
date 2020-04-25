from django.contrib import admin
from chat.models import *
# Register your models here.

admin.site.register(Users)
admin.site.register(Chat)
admin.site.register(Partecipants)
admin.site.register(Messages)
admin.site.register(Phonebook)
