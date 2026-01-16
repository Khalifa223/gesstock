from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.contrib import messages
from .models import Fournisseur

# Create your views here.
@login_required
def liste_fournisseurs(request):
    fournisseurs = Fournisseur.objects.all()
    paginator = Paginator(fournisseurs, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'page_obj': page_obj
    }
    return render(request, 'fournisseurs/liste_fournisseurs.html', context)

@login_required
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
        messages.success(request, f"Fournisseur {nom} ajouté avec succès")
        return redirect('liste_fournisseurs')

    return render(request, 'fournisseurs/ajouter_fournisseur.html', {'titre': 'Ajouter un fournisseur'})

@login_required
def modifier_fournisseur(request, id):
    fournisseur = get_object_or_404(Fournisseur, id=id)

    if request.method == 'POST':
        fournisseur.nom = request.POST.get('nom')
        fournisseur.contact = request.POST.get('contact')
        fournisseur.adresse = request.POST.get('adresse')
        fournisseur.email = request.POST.get('email')
        fournisseur.save()
        messages.success(request, f"Fournisseur {fournisseur.nom} modifié avec succès")
        return redirect('liste_fournisseurs')

    return render(request, 'fournisseurs/modifier_fournisseur.html', {
        'fournisseur': fournisseur,
        'titre': 'Modifier le fournisseur'
    })

@login_required
def supprimer_fournisseur(request, id):
    fournisseur = get_object_or_404(Fournisseur, id=id)
    if request.method == 'POST':
        fournisseur.delete()
        messages.success(request, f"Fournisseur supprimé avec succès")
        return redirect('liste_fournisseurs')
    return render(request, 'fournisseurs/supprimer_fournisseur.html', {'fournisseur': fournisseur})
