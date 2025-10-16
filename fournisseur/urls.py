from django.urls import path
from . import views

urlpatterns = [
    path('liste_fournisseurs/', views.liste_fournisseurs, name='liste_fournisseurs'),
    path('ajouter_fournisseur/', views.ajouter_fournisseur, name='ajouter_fournisseur'),
    path('modifier_fournisseur/', views.modifier_fournisseur, name='modifier_fournisseur'),
    path('supprimer_fournisseur/', views.supprimer_fournisseur, name='supprimer_fournisseur'),
]