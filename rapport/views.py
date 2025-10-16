from django.shortcuts import render
from .models import Rapport

# Create your views here.

def liste_rapports(request):
    rapports = Rapport.objects.select_related('genere_par').order_by('-date_generation')
    return render(request, 'rapports/liste_rapports.html', {'rapports': rapports})
