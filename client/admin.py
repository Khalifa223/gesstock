from django.contrib import admin
from .models import Client

# Register your models here.

# admin.site.register(Client)

class ClientAdmin(admin.ModelAdmin):
    list_display = ('nom', 'contact', 'adresse', 'email')
    

admin.site.register(Client, ClientAdmin)