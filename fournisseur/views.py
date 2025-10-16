from django.shortcuts import render, redirect, get_object_or_404
from .models import Fournisseur

# Create your views here.

def liste_fournisseurs(request):
    fournisseurs = Fournisseur.objects.all()
    return render(request, 'fournisseurs/liste_fournisseurs.html', {'fournisseurs': fournisseurs})


def ajouter_fournisseur(request):
    if request.method == 'POST':
        nom = request.POST.get('nom')
        contact = request.POST.get('contact')
        adresse = request.POST.get('adresse')
        email = request.POST.get('email')

        Fournisseur.objects.create(
            nom=nom,
            contact=contact,
            adresse=adresse,
            email=email
        )
        return redirect('liste_fournisseurs')

    return render(request, 'fournisseurs/ajouter_fournisseur.html', {'titre': 'Ajouter un fournisseur'})


def modifier_fournisseur(request, id):
    fournisseur = get_object_or_404(Fournisseur, id=id)

    if request.method == 'POST':
        fournisseur.nom = request.POST.get('nom')
        fournisseur.contact = request.POST.get('contact')
        fournisseur.adresse = request.POST.get('adresse')
        fournisseur.email = request.POST.get('email')
        fournisseur.save()
        return redirect('liste_fournisseurs')

    return render(request, 'fournisseurs/modifier_fournisseur.html', {
        'fournisseur': fournisseur,
        'titre': 'Modifier le fournisseur'
    })


def supprimer_fournisseur(request, id):
    fournisseur = get_object_or_404(Fournisseur, id=id)
    if request.method == 'POST':
        fournisseur.delete()
        return redirect('liste_fournisseurs')
    return render(request, 'fournisseurs/supprimer_fournisseur.html', {'fournisseur': fournisseur})
