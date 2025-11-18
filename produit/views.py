from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Avg, Min, Max
from django.http import HttpResponse
import io
import barcode
from barcode.writer import ImageWriter
from .models import Produit, Categorie


# Create your views here.

@login_required
def liste_produits(request):
    produits = Produit.objects.select_related('categorie').all()
    return render(request, 'produits/liste_produits.html', {'produits': produits})

@login_required
def ajouter_produit(request):
    categories = Categorie.objects.all()

    if request.method == 'POST':
        nom = request.POST.get('nom')
        categorie_id = request.POST.get('categorie')
        prix_achat = request.POST.get('prix_achat')
        prix_vente = request.POST.get('prix_vente')
        seuil_min = request.POST.get('seuil_min')
        seuil_max = request.POST.get('seuil_max')
        stock_actuel = request.POST.get('stock_actuel')
        
        # Verifie si la categorie existe
        categorie = Categorie.objects.get(id=categorie_id) if categorie_id else None
        
        # Génération automatique de référence (ex: PROD-00123)
        dernier_id = Produit.objects.last().id + 1 if Produit.objects.exists() else 1
        reference = f"PROD-{dernier_id:05d}"

        # Génération du code-barres à partir de la référence
        buffer = io.BytesIO()
        barcode_format = barcode.get_barcode_class('code128')
        barcode_obj = barcode_format(reference, writer=ImageWriter())
        barcode_obj.write(buffer)
        code_barre = f"{reference}.png"
        

        Produit.objects.create(
            nom=nom,
            reference=reference,
            categorie=categorie,
            prix_achat=prix_achat or 0,
            prix_vente=prix_vente or 0,
            code_barre_image=code_barre,
            seuil_min=seuil_min or 0,
            seuil_max=seuil_max or 0,
            stock_actuel=stock_actuel or 0
        )

        return redirect('liste_produits')

    return render(request, 'produits/ajouter_produit.html', {
        'categories': categories,
        'titre': 'Ajouter un produit'
    })

@login_required
def modifier_produit(request, id):
    produit = get_object_or_404(Produit, id=id)
    categories = Categorie.objects.all()

    if request.method == 'POST':
        produit.nom = request.POST.get('nom')
        categorie_id = request.POST.get('categorie')
        produit.categorie = Categorie.objects.get(id=categorie_id) if categorie_id else None
        produit.prix_achat = request.POST.get('prix_achat') or 0
        produit.prix_vente = request.POST.get('prix_vente') or 0
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

@login_required
def supprimer_produit(request, id):
    produit = get_object_or_404(Produit, id=id)
    if request.method == 'POST':
        produit.delete()
        return redirect('liste_produits')

    return render(request, 'produits/supprimer_produit.html', {'produit': produit})

@login_required
def suivi_prix(request):
    """
    Fournit un tableau de bord du suivi des prix d’achat et de vente :
    - prix moyen d’achat et de vente
    - produit le plus cher / le moins cher
    - marge moyenne (prix_vente - prix_achat)
    """
    produits = Produit.objects.all()

    statistiques = {
        'prix_achat_moyen': produits.aggregate(Avg('prix_achat'))['prix_achat__avg'] or 0,
        'prix_vente_moyen': produits.aggregate(Avg('prix_vente'))['prix_vente__avg'] or 0,
        'prix_achat_min': produits.aggregate(Min('prix_achat'))['prix_achat__min'] or 0,
        'prix_vente_max': produits.aggregate(Max('prix_vente'))['prix_vente__max'] or 0,
    }

    # Calcul des marges pour chaque produit
    marges = []
    for p in produits:
        marge = float(p.prix_vente or 0) - float(p.prix_achat or 0)
        marges.append({'produit': p, 'marge': marge})

    return render(request, 'produits/suivi_prix.html', {
        'statistiques': statistiques,
        'marges': marges,
        'titre': 'Suivi des prix d’achat et de vente'
    })


# ==========================================================
# CATEGORIES 
# ==========================================================
@login_required
def liste_categories(request):
    categories = Categorie.objects.all()
    return render(request, 'produits/categories/liste_categories.html', {'categories': categories})

@login_required
def ajouter_categorie(request):
    if request.method == 'POST':
        nom = request.POST.get('nom')
        description = request.POST.get('description')
        Categorie.objects.create(nom=nom, description=description)
        return redirect('liste_categories')

    return render(request, 'produits/categories/ajouter_categorie.html', {'titre': 'Ajouter une catégorie'})

@login_required
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

@login_required
def supprimer_categorie(request, id):
    categorie = get_object_or_404(Categorie, id=id)
    if request.method == 'POST':
        categorie.delete()
        return redirect('liste_categories')

    return render(request, 'produits/categories/supprimer_categorie.html', {'categorie': categorie})

@login_required
# Catégoriser les produits 
def categoriser_produits(request):
    """
    Permet d'afficher les produits regroupés par catégorie
    (visualisation hiérarchique des familles et sous-familles de produits).
    """
    categories = Categorie.objects.prefetch_related('produits').all()
    return render(request, 'produits/categorisation.html', {
        'categories': categories,
        'titre': 'Catégorisation des produits'
    })
    

# ==========================================================
#   TÉLÉCHARGEMENT DU CODE-BARRES
# ==========================================================
@login_required
def telecharger_code_barres(request, id):
    """
    Génère et renvoie l’image du code-barres du produit sélectionné.
    """
    produit = get_object_or_404(Produit, id=id)

    buffer = io.BytesIO()
    barcode_format = barcode.get_barcode_class('code128')
    barcode_obj = barcode_format(produit.reference, writer=ImageWriter())
    barcode_obj.write(buffer)

    response = HttpResponse(buffer.getvalue(), content_type='image/png')
    response['Content-Disposition'] = f'attachment; filename="{produit.reference}.png"'
    return response