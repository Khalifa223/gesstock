from django.urls import path
from . import views

urlpatterns = [
    path('liste_mouvements/', views.liste_mouvements, name='liste_mouvements'),
    path('ajouter_entree/', views.ajouter_entree, name='ajouter_entree'),
    path('ajouter_sortie/', views.ajouter_sortie, name='ajouter_sortie'),
    path('modifier_mouvement/', views.modifier_mouvement, name='modifier_mouvement'),
    path('supprimer_mouvement/', views.supprimer_mouvement, name='supprimer_mouvement'),
    path('tableau_stock/', views.tableau_stock, name='tableau_stock'),
]