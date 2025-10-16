from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import MouvementStock
from produit.models import Produit
from fournisseur.models import Fournisseur
from client.models import Client

# Create your views here.

def liste_mouvements(request):
    mouvements = MouvementStock.objects.select_related('produit', 'utilisateur', 'fournisseur', 'client').order_by('-date_mouvement')
    return render(request, 'stocks/liste_mouvements.html', {'mouvements': mouvements})


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

        messages.success(request, f"Entrée enregistrée : +{quantite} unités pour {produit.nom}")
        return redirect('liste_mouvements')

    return render(request, 'stocks/ajouter_entree.html', {
        'produits': produits,
        'fournisseurs': fournisseurs,
        'titre': 'Nouvelle entrée de stock'
    })
    

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

        messages.success(request, f"Sortie enregistrée : -{quantite} unités pour {produit.nom}")
        return redirect('liste_mouvements')

    return render(request, 'stocks/ajouter_sortie.html', {
        'produits': produits,
        'clients': clients,
        'titre': 'Nouvelle sortie de stock'
    })


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


def supprimer_mouvement(request, id):
    mouvement = get_object_or_404(MouvementStock, id=id)
    produit = mouvement.produit

    if request.method == 'POST':
        # Réajustement du stock selon le type
        if mouvement.type_mouvement == 'ENTREE':
            produit.stock_actuel -= mouvement.quantite
        elif mouvement.type_mouvement == 'SORTIE':
            produit.stock_actuel += mouvement.quantite

        produit.save()
        mouvement.delete()

        messages.success(request, f"Mouvement supprimé et stock de {produit.nom} mis à jour.")
        return redirect('liste_mouvements')

    return render(request, 'stocks/supprimer_mouvement.html', {'mouvement': mouvement})


def tableau_stock(request):
    produits = Produit.objects.select_related('categorie').all()
    return render(request, 'stocks/tableau_stock.html', {'produits': produits})
