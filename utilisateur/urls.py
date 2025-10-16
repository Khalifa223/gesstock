from django.urls import path
from . import views

urlpatterns = [
    path('ajouter_utilisateur/', views.ajouter_utilisateur, name='ajouter_utilisateur'), 
]