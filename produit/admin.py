from django.contrib import admin
from .models import Produit, Categorie

# Register your models here.

class ProduitAdmin(admin.ModelAdmin):
    list_display = ('nom', 'categorie', 'prix_achat', 'prix_vente', 'stock_actuel')
    
class CategorieAdmin(admin.ModelAdmin):
    list_display = ('nom', 'description')    

admin.site.register(Produit, ProduitAdmin)
admin.site.register(Categorie, CategorieAdmin)