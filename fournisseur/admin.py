from django.contrib import admin
from .models import Fournisseur

# Register your models here.

class FournisseurAdmin(admin.ModelAdmin):
    list_display = ('nom', 'contact', 'adresse', 'email')
    

admin.site.register(Fournisseur, FournisseurAdmin)