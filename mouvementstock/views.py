from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, F, Count
from django.contrib import messages
from .models import MouvementStock
from produit.models import Produit
from fournisseur.models import Fournisseur
from utilisateur.models import Utilisateur
from client.models import Client

# Create your views here.

@login_required
def liste_mouvements(request):
    mouvements = MouvementStock.objects.select_related('produit', 'utilisateur', 'fournisseur', 'client').order_by('-date_mouvement')
    produits = Produit.objects.select_related('categorie').all()
    
    for produit in produits:
        if produit.stock_actuel <= produit.seuil_min:
            messages.warning(request, f"Le produit '{produit.nom}' est en rupture ou proche du seuil minimum.")
        elif produit.stock_actuel >= produit.seuil_max:
            messages.warning(request, f"Le produit '{produit.nom}' dépasse le seuil maximum défini.")
    
    return render(request, 'stocks/liste_mouvements.html', {'mouvements': mouvements})

@login_required
def liste_stocks(request):
    """
    Afficher la liste des produits avec leurs niveaux de stock
    et les éventuelles alertes (rupture ou surstock).
    """
    produits = Produit.objects.select_related('categorie').all()
    alertes = []

    for produit in produits:
        if produit.stock_actuel <= produit.seuil_min:
            alertes.append({
                'type': 'danger',
                'message': f"Le produit '{produit.nom}' est en rupture ou proche du seuil minimum."
            })
        elif produit.stock_actuel >= produit.seuil_max:
            alertes.append({
                'type': 'warning',
                'message': f"Le produit '{produit.nom}' dépasse le seuil maximum défini."
            })

    return render(request, 'stock/liste_stocks.html', {
        'produits': produits,
        'alertes': alertes,
        'titre': 'Gestion des Stocks'
    })
    
@login_required
def ajouter_entree(request):
    produits = Produit.objects.all()
    fournisseurs = Fournisseur.objects.all()

    if request.method == 'POST':
        produit_id = request.POST.get('produit')
        quantite = int(request.POST.get('quantite') or 0)
        commentaire = request.POST.get('commentaire')
        fournisseur_id = request.POST.get('fournisseur')

        produit = get_object_or_404(Produit, id=produit_id)
        fournisseur = Fournisseur.objects.get(id=fournisseur_id) if fournisseur_id else None

        # Créer le mouvement
        mouvement = MouvementStock.objects.create(
            produit=produit,
            type_mouvement='ENTREE',
            quantite=quantite,
            commentaire=commentaire,
            utilisateur=request.user,
            fournisseur=fournisseur
        )

        # Mise à jour du stock
        produit.stock_actuel += quantite
        produit.save()

        # Vérification des alertes
        if produit.stock_actuel >= produit.seuil_max:
            messages.warning(request, f"Alerte : Le produit '{produit.nom}' a atteint le seuil maximum.")
        else:
            messages.success(request, f"Entrée enregistrée : {quantite} unité(s) ajoutée(s) à '{produit.nom}'.")
        return redirect('liste_mouvements')

    return render(request, 'stocks/ajouter_entree.html', {
        'produits': produits,
        'fournisseurs': fournisseurs,
        'titre': 'Nouvelle entrée de stock'
    })
    
@login_required
def ajouter_sortie(request):
    produits = Produit.objects.all()
    clients = Client.objects.all()

    if request.method == 'POST':
        produit_id = request.POST.get('produit')
        quantite = int(request.POST.get('quantite') or 0)
        commentaire = request.POST.get('commentaire')
        client_id = request.POST.get('client')

        produit = get_object_or_404(Produit, id=produit_id)
        client = Client.objects.get(id=client_id) if client_id else None

        if quantite > produit.stock_actuel:
            messages.error(request, f"Stock insuffisant pour {produit.nom} (stock actuel : {produit.stock_actuel})")
            return redirect('ajouter_sortie')

        # Créer le mouvement
        mouvement = MouvementStock.objects.create(
            produit=produit,
            type_mouvement='SORTIE',
            quantite=quantite,
            commentaire=commentaire,
            utilisateur=request.user,
            client=client
        )

        # Mise à jour du stock
        produit.stock_actuel -= quantite
        produit.save()
        
        # Vérification des alertes
        if produit.stock_actuel <= produit.seuil_min:
            messages.error(request, f"Alerte : Le produit '{produit.nom}' est en dessous du seuil minimum.")
        else:
            messages.success(request, f"Sortie enregistrée : {quantite} unité(s) retirée(s) de '{produit.nom}'.")
        return redirect('liste_mouvements')

    return render(request, 'stocks/ajouter_sortie.html', {
        'produits': produits,
        'clients': clients,
        'titre': 'Nouvelle sortie de stock'
    })

@login_required
def modifier_mouvement(request, id):
    mouvement = get_object_or_404(MouvementStock, id=id)
    produits = Produit.objects.all()
    fournisseurs = Fournisseur.objects.all()
    clients = Client.objects.all()

    if request.method == 'POST':
        ancien_produit = mouvement.produit
        ancienne_quantite = mouvement.quantite
        ancien_type = mouvement.type_mouvement

        produit_id = request.POST.get('produit')
        quantite = int(request.POST.get('quantite') or 0)
        commentaire = request.POST.get('commentaire')

        # Mettre à jour le mouvement
        mouvement.produit = get_object_or_404(Produit, id=produit_id)
        mouvement.quantite = quantite
        mouvement.commentaire = commentaire
        mouvement.save()

        # Réajuster le stock si produit ou quantité a changé
        if ancien_type == 'ENTREE':
            ancien_produit.stock_actuel -= ancienne_quantite
        else:
            ancien_produit.stock_actuel += ancienne_quantite

        if mouvement.type_mouvement == 'ENTREE':
            mouvement.produit.stock_actuel += quantite
        else:
            mouvement.produit.stock_actuel -= quantite

        ancien_produit.save()
        mouvement.produit.save()

        messages.success(request, f"Mouvement mis à jour pour {mouvement.produit.nom}")
        return redirect('liste_mouvements')

    return render(request, 'stocks/modifier_mouvement.html', {
        'mouvement': mouvement,
        'produits': produits,
        'fournisseurs': fournisseurs,
        'clients': clients,
        'titre': 'Modifier le mouvement de stock'
    })

@login_required
def supprimer_mouvement(request, id):
    mouvement = get_object_or_404(MouvementStock, id=id)
    produit = mouvement.produit

    # if request.method == 'POST':
        # Réajustement du stock selon le type
    if mouvement.type_mouvement == 'ENTREE':
        produit.stock_actuel -= mouvement.quantite
    elif mouvement.type_mouvement == 'SORTIE':
        produit.stock_actuel += mouvement.quantite

    produit.save()
    mouvement.delete()

    messages.success(request, f"Mouvement supprimé et stock de {produit.nom} mis à jour.")
    return redirect('liste_mouvements')

    # return render(request, 'stocks/supprimer_mouvement.html', {'mouvement': mouvement})

@login_required
def tableau_stock(request):
    produits = Produit.objects.select_related('categorie').all()
    return render(request, 'stocks/tableau_stock.html', {'produits': produits})

@login_required
def consultation_stocks(request):
    """
    Affiche la liste de tous les produits avec leurs niveaux de stock en temps réel.
    Met aussi en évidence les produits en rupture ou en surstock.
    """
    produits = Produit.objects.select_related('categorie').all()

    # Détection des produits en rupture ou en surstock
    ruptures = produits.filter(stock_actuel__lte=F('seuil_min'))
    surstocks = produits.filter(stock_actuel__gte=F('seuil_max'))

    contexte = {
        'produits': produits,
        'ruptures': ruptures,
        'surstocks': surstocks,
        'titre': 'Consultation du stock en temps réel',
    }

    return render(request, 'stocks/consultation_stocks.html', contexte)

@login_required
def produits_en_alerte(request):
    """
    Liste les produits dont le niveau de stock est inférieur ou égal au seuil minimum (alerte de rupture)
    ou supérieur au seuil maximum (alerte de surstock).
    """
    produits_rupture = Produit.objects.filter(stock_actuel__lte=F('seuil_min'))
    produits_surstocks = Produit.objects.filter(stock_actuel__gte=F('seuil_max'))

    contexte = {
        'produits_rupture': produits_rupture,
        'produits_surstocks': produits_surstocks,
        'titre': 'Alertes de stock',
    }

    return render(request, 'stocks/produits_en_alerte.html', contexte)


# ==========================================================
# 🔄 LES PRODUITS LES PLUS VENDUS
# ==========================================================
@login_required
def produits_plus_vendus(request):
    """
    Statistiques détaillées sur les produits les plus vendus.
    """
    produits_plus_vendus = (
        MouvementStock.objects
        .filter(type_mouvement='SORTIE')
        .values('produit__nom', 'produit__categorie__nom')
        .annotate(total_vendu=Sum('quantite'))
        .order_by('-total_vendu')
    )

    return render(request, 'rapports/produits_plus_vendus.html', {
        'produits_vendus': produits_plus_vendus,
        'titre': 'Produits les plus vendus'
    })

# ==========================================================
# 🔄 LES FOURNISEURS LES PLUS UTILISES
# ==========================================================
@login_required
def fournisseurs_plus_utilises(request):
    """
    Statistiques détaillées sur les fournisseurs les plus sollicités.
    """
    fournisseurs_utilises = (
        MouvementStock.objects
        .filter(type_mouvement='ENTREE')
        .values('fournisseur__nom', 'fournisseur__contact')
        .annotate(total_entrees=Count('id'), quantite_totale=Sum('quantite'))
        .order_by('-quantite_totale')
    )

    return render(request, 'rapports/fournisseurs_plus_utilises.html', {
        'fournisseurs_utilises': fournisseurs_utilises,
        'titre': 'Fournisseurs les plus utilisés'
    })