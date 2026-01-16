from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.contrib import messages
from .models import Client


# Create your views here.

@login_required
def liste_clients(request):
    clients = Client.objects.all()
    paginator = Paginator(clients, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'clients': clients,
        'page_obj': page_obj
    }
    return render(request, 'clients/liste_clients.html', context)

@login_required
def ajouter_client(request):
    if request.method == 'POST':
        nom = request.POST.get('nom')
        contact = request.POST.get('contact')
        adresse = request.POST.get('adresse')
        email = request.POST.get('email')
        
        Client.objects.create(
            nom=nom,
            contact=contact,
            adresse=adresse,
            email=email
        )
        messages.success(request, f"client {nom} ajouté avec succès")
        return redirect('liste_clients')

    return render(request, 'clients/ajouter_client.html', {'titre': 'Ajouter un client'})

@login_required
def modifier_client(request, id):
    client = get_object_or_404(Client, id=id)

    if request.method == 'POST':
        client.nom = request.POST.get('nom')
        client.contact = request.POST.get('contact')
        client.adresse = request.POST.get('adresse')
        client.email = request.POST.get('email')
        client.save()
        messages.success(request, f"Client {client.nom} modifié avec succès")
        return redirect('liste_clients')

    return render(request, 'clients/modifier_client.html', {
        'client': client,
        'titre': 'Modifier le client'
    })

@login_required
def supprimer_client(request, id):
    client = get_object_or_404(Client, id=id)
    if request.method == 'POST':
        client.delete()
        messages.success(request, f"Client supprimé avec succès")
        return redirect('liste_clients')
    
    return render(request, 'clients/supprimer_client.html', {'client': client})
