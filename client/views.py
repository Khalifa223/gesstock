from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Client


# Create your views here.

@login_required
def liste_clients(request):
    clients = Client.objects.all()
    return render(request, 'clients/liste_clients.html', {'clients': clients})

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
        return redirect('liste_clients')
    return render(request, 'clients/supprimer_client.html', {'client': client})
