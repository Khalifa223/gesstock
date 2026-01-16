from django.urls import path
from . import views

urlpatterns = [
    path('liste_produits/', views.liste_produits, name='liste_produits'), 
    path('ajouter_produit/', views.ajouter_produit, name='ajouter_produit'), 
    path('modifier_produit/<int:id>/', views.modifier_produit, name='modifier_produit'), 
    path('supprimer_produit/<int:id>/', views.supprimer_produit, name='supprimer_produit'),
    path('suivi_prix/', views.suivi_prix, name='suivi_prix'),
    path('detail_produit/<int:id>/', views.detail_produit, name='detail_produit'),
    path('categorisations/', views.categoriser_produits, name='categorisation'),
    
    path('categories/liste_categories/', views.liste_categories, name='liste_categories'),
    path('categories/ajouter_categorie/', views.ajouter_categorie, name='ajouter_categorie'),
    path('categories/modifier_categorie/<int:id>/', views.modifier_categorie, name='modifier_categorie'),
    path('categories/supprimer_categorie/<int:id>/', views.supprimer_categorie, name='supprimer_categorie')
]