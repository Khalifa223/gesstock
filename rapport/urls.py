from django.urls import path
from . import views

urlpatterns = [
    path('liste_rapports/', views.liste_rapports, name='liste_rapports'),
    path('details_rapports/', views.details_rapport, name='details_rapport'),
    path('supprimer_rapports/<int:id>/', views.supprimer_rapport, name='supprimer_rapport'),
    path('generer_rapports/', views.generer_rapport, name='generer_rapport'),
    path('exporter/csv/<int:id>/', views.exporter_rapport_csv, name='exporter_rapport_csv'),
    path('exporter/excel/<int:id>/', views.exporter_rapport_excel, name='exporter_rapport_excel'),
    path('exporter/pdf/<int:id>/', views.exporter_rapport_pdf, name='exporter_rapport_pdf'),
]