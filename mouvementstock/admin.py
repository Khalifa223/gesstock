from django.contrib import admin
from .models import MouvementStock

# Register your models here.

class MouvementStockAdmin(admin.ModelAdmin):
    list_display = ('produit', 'type_mouvement', 'quantite', 'date_mouvement', 'commentaire', 'utilisateur', 'fournisseur', 'client')
    

admin.site.register(MouvementStock, MouvementStockAdmin)