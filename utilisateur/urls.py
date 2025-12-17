from django.urls import path
from . import views

urlpatterns = [
    path('connexion_utilisateur/', views.connexion_utilisateur, name='connexion_utilisateur'),
    path('deconnexion_utilisateur/', views.deconnexion_utilisateur, name='deconnexion_utilisateur'),
    path('ajouter_utilisateur/', views.ajouter_utilisateur, name='ajouter_utilisateur'),
    path('liste_utilisateurs/', views.liste_utilisateurs, name='liste_utilisateurs'),
    path('modifier_utilisateur/<int:id>/', views.modifier_utilisateur, name='modifier_utilisateur'),
    path('supprimer_utilisateur/<int:id>/', views.supprimer_utilisateur, name='supprimer_utilisateur'),
    path('profil_utilisateur/', views.profil_utilisateur, name='profil_utilisateur'),
    path('modifier_profil_utilisateur/', views.modifier_profil_utilisateur, name='modifier_profil_utilisateur'),
    path('change_password_utilisateur/', views.change_password_utilisateur, name='change_password_utilisateur'),
]