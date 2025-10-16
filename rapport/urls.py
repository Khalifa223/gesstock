from django.urls import path
from . import views

urlpatterns = [
    path('liste_rapports/', views.liste_rapports, name='liste_rapports'), 
]