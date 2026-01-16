from django.shortcuts import render
from django.db.models import Sum, Avg, Count, F, FloatField
from django.utils import timezone
from django.db.models.functions import TruncDate
from django.contrib.auth.decorators import login_required
from utilisateur.models import Utilisateur
from produit.models import Produit
from mouvementstock.models import MouvementStock
from datetime import timedelta
# Create your views here.

@login_required
def dashboard(request):
    """
    Vue du tableau de bord principal GesStock
    Fournit les statistiques globales, graphiques et suivi en temps réel.
    """

    # --- Période d’analyse (30 derniers jours)
    today = timezone.now()
    start_date = today - timedelta(days=30)

    # --- Données globales (KPI)
    total_produits = Produit.objects.count()
    stock_total = Produit.objects.aggregate(total=Sum('stock_actuel'))['total'] or 0
    valeur_stock = Produit.objects.aggregate(
        total=Sum(F('stock_actuel') * F('prix_achat'), output_field=FloatField())
    )['total'] or 0

    mouvements_entree = MouvementStock.objects.filter(
        type_mouvement='ENTREE', date_mouvement__gte=start_date
    ).count()

    mouvements_sortie = MouvementStock.objects.filter(
        type_mouvement='SORTIE', date_mouvement__gte=start_date
    ).count()

    produits_alerte = Produit.objects.filter(
        stock_actuel__lte=F('seuil_min')
    ).count()

    marge_moyenne = Produit.objects.aggregate(
        moyenne=Avg(F('prix_vente') - F('prix_achat'), output_field=FloatField())
    )['moyenne'] or 0
    
    # --- Évolution entrées / sorties sur 30 jours
    mouvements_30j = (
        MouvementStock.objects.filter(date_mouvement__gte=start_date)
        .annotate(date_simple=TruncDate('date_mouvement'))
        .values('date_simple', 'type_mouvement')
        .annotate(total=Sum('quantite'))
        .order_by('date_simple')
    )
    
     # Regroupement par jour
    evolution_dict = {}
    for m in mouvements_30j:
        date = m['date_simple'].strftime('%d/%m')
        if date not in evolution_dict:
            evolution_dict[date] = {'ENTREE': 0, 'SORTIE': 0}
        evolution_dict[date][m['type_mouvement']] = m['total'] or 0

    dates_labels = list(evolution_dict.keys())
    entrees_values = [evolution_dict[d]['ENTREE'] for d in dates_labels]
    sorties_values = [evolution_dict[d]['SORTIE'] for d in dates_labels]

    # --- Derniers mouvements (suivi en temps réel)
    derniers_mouvements = MouvementStock.objects.select_related('produit', 'utilisateur').order_by('-date_mouvement')[:10]

    mouvements_data = [
        {
            'date': m.date_mouvement.strftime('%d/%m/%Y %H:%M'),
            'type': 'Entrée' if m.type_mouvement == 'ENTREE' else 'Sortie',
            'produit': m.produit.nom,
            'quantite': m.quantite,
            'utilisateur': m.utilisateur.username if m.utilisateur else '—',
            'commentaire': m.commentaire or ''
        }
        for m in derniers_mouvements
    ]

    # --- Répartition par catégorie
    categories_data = list(
        Produit.objects.values('categorie__nom')
        .annotate(total=Sum('stock_actuel'))
        .order_by('-total')
    )
    categories_chart = [
        {'label': c['categorie__nom'] or 'Autre', 'value': c['total'] or 0}
        for c in categories_data
    ]

    # --- Top 5 des produits les plus vendus
    top_ventes = list(
        MouvementStock.objects.filter(type_mouvement='SORTIE')
        .values('produit__nom')
        .annotate(total_vendus=Sum('quantite'))
        .order_by('-total_vendus')[:5]
    )
    top_produits_chart = [
        {'label': t['produit__nom'], 'value': t['total_vendus']} for t in top_ventes
    ]
    
    # --- Top 5 des produits les plus vendus
    top_fournisseurs = list(
        MouvementStock.objects.filter(type_mouvement='ENTREE')
        .values('fournisseur__nom')
        .annotate(fournisseur_utilise=Sum('quantite'))
        .order_by('fournisseur_utilise')[:5]
    )
    top_fournisseurs_chart = [
        {'label': t['fournisseur__nom'], 'value': t['fournisseur_utilise']} for t in top_fournisseurs
    ]

    # --- Valeur du stock par fournisseur
    fournisseurs_data = list(
        Produit.objects.values('mouvements')
        .annotate(valeur=Sum(F('stock_actuel') * F('prix_achat'), output_field=FloatField()))
        .order_by('-valeur')[:5]
    )
    # fournisseurs_chart = [
    #     {'label': f['mouvements'] or 'Inconnu', 'value': f['valeur'] or 0}
    #     for f in fournisseurs_data
    # ]

    # --- Utilisateurs les plus actifs
    utilisateurs_actifs = list(
        MouvementStock.objects.values('utilisateur__username')
        .annotate(actions=Count('id'))
        .order_by('-actions')[:5]
    )
    utilisateurs_data = [
        {
            'nom': u['utilisateur__username'] or 'Anonyme',
            'initiale': (u['utilisateur__username'] or '?')[0].upper(),
            'actions': u['actions'],
            'derniere_activite': MouvementStock.objects.filter(utilisateur__username=u['utilisateur__username'])
                .order_by('-date_mouvement')
                .values_list('date_mouvement', flat=True)
                .first()
                .strftime('%d/%m/%Y %H:%M') if u['utilisateur__username'] else '—'
        }
        for u in utilisateurs_actifs
    ]

    # --- Alertes de stock
    alertes_stock = list(
        Produit.objects.filter(stock_actuel__lte=F('seuil_min'))
        .values('nom', 'stock_actuel', 'seuil_min')
    )

    alertes = [
        {
            'texte': f"Stock faible : {a['nom']} ({a['stock_actuel']} restants, seuil {a['seuil_min']})",
            'type': 'low'
        }
        for a in alertes_stock
    ]

    # --- Contexte complet pour le template
    contexte = {
        'titre': 'Tableau de bord - GesStock',
        'kpis': {
            'produits_total': total_produits,
            'stock_total': stock_total,
            'valeur_stock': valeur_stock,
            'stocks_entree': mouvements_entree,
            'stocks_sortie': mouvements_sortie,
            # 'produits_alerte': produits_alerte,
            'marge_moyenne': round(marge_moyenne, 2)
        },
        'evolution': {
            'dates': dates_labels,
            'entrees': entrees_values,
            'sorties': sorties_values
        },
        'mouvements': mouvements_data,
        'categories': categories_chart,
        'top_produits': top_produits_chart,
        'fournisseurs': top_fournisseurs_chart,
        # 'fournisseurs': fournisseurs_chart,
        # 'utilisateurs': utilisateurs_data,
        # 'alertes': alertes,
    }

    return render(request, 'gesstock/dashboard.html', contexte)
