from django.shortcuts import render, redirect, get_object_or_404
from .models import Produit, Categorie

# Create your views here.

def liste_produits(request):
    """Afficher la liste de tous les produits"""
    produits = Produit.objects.select_related('categorie').all()
    return render(request, 'produits/liste.html', {'produits': produits})


def ajouter_produit(request):
    categories = Categorie.objects.all()

    if request.method == 'POST':
        nom = request.POST.get('nom')
        reference = request.POST.get('reference')
        categorie_id = request.POST.get('categorie')
        prix_achat = request.POST.get('prix_achat')
        prix_vente = request.POST.get('prix_vente')
        code_barre = request.POST.get('code_barre')
        seuil_min = request.POST.get('seuil_min')
        seuil_max = request.POST.get('seuil_max')
        stock_actuel = request.POST.get('stock_actuel')

        categorie = Categorie.objects.get(id=categorie_id) if categorie_id else None

        Produit.objects.create(
            nom=nom,
            reference=reference,
            categorie=categorie,
            prix_achat=prix_achat or 0,
            prix_vente=prix_vente or 0,
            code_barre=code_barre,
            seuil_min=seuil_min or 0,
            seuil_max=seuil_max or 0,
            stock_actuel=stock_actuel or 0
        )

        return redirect('liste_produits')

    return render(request, 'produits/ajouter_produit.html', {
        'categories': categories,
        'titre': 'Ajouter un produit'
    })


def modifier_produit(request, id):
    produit = get_object_or_404(Produit, id=id)
    categories = Categorie.objects.all()

    if request.method == 'POST':
        produit.nom = request.POST.get('nom')
        produit.reference = request.POST.get('reference')
        categorie_id = request.POST.get('categorie')
        produit.categorie = Categorie.objects.get(id=categorie_id) if categorie_id else None
        produit.prix_achat = request.POST.get('prix_achat') or 0
        produit.prix_vente = request.POST.get('prix_vente') or 0
        produit.code_barre = request.POST.get('code_barre')
        produit.seuil_min = request.POST.get('seuil_min') or 0
        produit.seuil_max = request.POST.get('seuil_max') or 0
        produit.stock_actuel = request.POST.get('stock_actuel') or 0
        produit.save()

        return redirect('liste_produits')

    return render(request, 'produits/modifier_produit.html', {
        'produit': produit,
        'categories': categories,
        'titre': 'Modifier le produit'
    })


def supprimer_produit(request, id):
    """Supprimer un produit"""
    produit = get_object_or_404(Produit, id=id)
    if request.method == 'POST':
        produit.delete()
        return redirect('liste_produits')

    return render(request, 'produits/supprimer_produit.html', {'produit': produit})


# ==========================================================
# CATEGORIES 
# ==========================================================

def liste_categories(request):
    categories = Categorie.objects.all()
    return render(request, 'produits/categories/liste_categories.html', {'categories': categories})


def ajouter_categorie(request):
    if request.method == 'POST':
        nom = request.POST.get('nom')
        description = request.POST.get('description')
        Categorie.objects.create(nom=nom, description=description)
        return redirect('liste_categories')

    return render(request, 'produits/categories/ajouter_categorie.html', {'titre': 'Ajouter une catégorie'})


def modifier_categorie(request, id):
    categorie = get_object_or_404(Categorie, id=id)

    if request.method == 'POST':
        categorie.nom = request.POST.get('nom')
        categorie.description = request.POST.get('description')
        categorie.save()
        return redirect('liste_categories')

    return render(request, 'produits/categories/modifier_categorie.html', {
        'categorie': categorie,
        'titre': 'Modifier la catégorie'
    })


def supprimer_categorie(request, id):
    categorie = get_object_or_404(Categorie, id=id)
    if request.method == 'POST':
        categorie.delete()
        return redirect('liste_categories')

    return render(request, 'produits/categories/supprimer_categorie.html', {'categorie': categorie})
