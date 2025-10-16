from django.urls import path
from . import views

urlpatterns = [
    path('liste_clients/', views.liste_clients, name='liste_clients'),
    path('ajouter_client/', views.ajouter_client, name='ajouter_client'),
    path('modifier_client/', views.modifier_client, name='modifier_client'),
    path('supprimer_client/', views.supprimer_client, name='supprimer_client'),
]