from django.urls import path
from . import views

urlpatterns = [
    path('liste_mouvements/', views.liste_mouvements, name='liste_mouvements'),
    path('ajouter_entree/', views.ajouter_entree, name='ajouter_entree'),
    path('ajouter_sortie/', views.ajouter_sortie, name='ajouter_sortie'),
    path('modifier_mouvement/<int:id>/', views.modifier_mouvement, name='modifier_mouvement'),
    path('supprimer_mouvement/<int:id>/', views.supprimer_mouvement, name='supprimer_mouvement'),
    path('tableau_stock/', views.tableau_stock, name='tableau_stock'),
    path('consultation_stocks/', views.consultation_stocks, name='consultation_stocks'),
    # path('produits_en_alerte/', views.produits_en_alerte, name='produits_en_alerte'),
    # path('produits_plus_vendus/', views.produits_plus_vendus, name='produits_plus_vendus'),
    # path('fournisseurs_plus_utilises/', views.fournisseurs_plus_utilises, name='fournisseurs_plus_utilises'),
]