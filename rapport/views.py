from django.contrib.auth.decorators import login_required

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse
from django.utils import timezone
from .models import Rapport, MouvementStock, Produit
import csv
import io
from openpyxl import Workbook
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet

# Create your views here.

@login_required
def liste_rapports(request):
    rapports = Rapport.objects.select_related('genere_par').order_by('-date_generation')
    return render(request, 'rapports/liste_rapports.html', {'rapports': rapports})

@login_required
def details_rapport(request, id):
    """
    Afficher le contenu détaillé d’un rapport.
    """
    rapport = get_object_or_404(Rapport, id=id)
    mouvements = rapport.mouvements.select_related('produit', 'utilisateur').all()
    produits = rapport.produits.all()

    return render(request, 'rapports/details_rapport.html', {
        'rapport': rapport,
        'mouvements': mouvements,
        'produits': produits,
        'titre': f"Détails du {rapport.get_type_rapport_display()}"
    })

@login_required
def supprimer_rapport(request, id):
    """
    Supprimer un rapport existant.
    """
    rapport = get_object_or_404(Rapport, id=id)
    if request.method == 'POST':
        rapport.delete()
        messages.success(request, "Rapport supprimé avec succès.")
        return redirect('liste_rapports')

    return render(request, 'rapports/supprimer_rapport.html', {'rapport': rapport})

@login_required
def generer_rapport(request):
    """
    Génère un nouveau rapport en fonction du type choisi.
    """
@login_required(login_url='/utilisateurs/connexion_utilisateur/')
def generer_rapport(request):
    if request.method == 'POST':
        type_rapport = request.POST.get('type_rapport')

        # Récupération des données selon le type
        if type_rapport == 'VENTES':
            mouvements = MouvementStock.objects.filter(type_mouvement='SORTIE')
            titre = "Rapport des ventes"
        elif type_rapport == 'ACHATS':
            mouvements = MouvementStock.objects.filter(type_mouvement='ENTREE')
            titre = "Rapport des achats"
        elif type_rapport == 'PERTE':
            mouvements = MouvementStock.objects.filter(commentaire__icontains='perte')
            titre = "Rapport des pertes"
        else:
            mouvements = MouvementStock.objects.all()
            titre = "Rapport global du stock"

        # Création du rapport
        rapport = Rapport.objects.create(
            type_rapport=type_rapport,
            genere_par=request.user
        )
        rapport.mouvements.set(mouvements)
        produits = Produit.objects.filter(mouvements__in=mouvements).distinct()
        rapport.produits.set(produits)
        rapport.save()

        messages.success(request, f"{titre} généré avec succès.")
        return redirect('liste_rapports')

    return render(request, 'rapports/generer_rapport.html', {'titre': 'Générer un rapport'})

@login_required
def exporter_rapport_csv(request, id):
    """
    Exporter le contenu d’un rapport au format CSV.
    """
    rapport = get_object_or_404(Rapport, id=id)
    mouvements = rapport.mouvements.select_related('produit').all()

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'inline; filename="rapport_{rapport.type_rapport.lower()}_{rapport.id}.csv"'

    writer = csv.writer(response)
    writer.writerow(['Produit', 'Type de mouvement', 'Quantité', 'Date', 'Utilisateur'])

    for m in mouvements:
        writer.writerow([
            m.produit.nom,
            m.get_type_mouvement_display(),
            m.quantite,
            timezone.localtime(m.date_mouvement).strftime('%d/%m/%Y %H:%M'),
            m.utilisateur.username if m.utilisateur else '-'
        ])

    return response

@login_required
def exporter_rapport_excel(request, id):
    """
    Exporter le contenu d’un rapport au format Excel (.xlsx)
    """
    rapport = get_object_or_404(Rapport, id=id)
    mouvements = rapport.mouvements.select_related('produit').all()

    wb = Workbook()
    ws = wb.active
    ws.title = "Rapport de stock"

    # En-tête
    ws.append(['Produit', 'Type de mouvement', 'Quantité', 'Date', 'Utilisateur'])

    # Contenu
    for m in mouvements:
        ws.append([
            m.produit.nom,
            m.get_type_mouvement_display(),
            m.quantite,
            timezone.localtime(m.date_mouvement).strftime('%d/%m/%Y %H:%M'),
            m.utilisateur.username if m.utilisateur else '-'
        ])

    # Réponse HTTP
    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = f'inline; filename="rapport_{rapport.type_rapport.lower()}_{rapport.id}.xlsx"'

    wb.save(response)
    return response

@login_required
def exporter_rapport_pdf(request, id):
    """
    Exporter le contenu d’un rapport au format PDF.
    """
    rapport = get_object_or_404(Rapport, id=id)
    mouvements = rapport.mouvements.select_related('produit').all()

    # Configuration de la réponse
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'inline; filename="rapport_{rapport.type_rapport.lower()}_{rapport.id}.pdf"'

    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4)
    story = []
    styles = getSampleStyleSheet()

    # Titre du rapport
    story.append(Paragraph(f"Rapport : {rapport.get_type_rapport_display()}", styles["Title"]))
    story.append(Paragraph(f"Date de génération : {timezone.localtime(rapport.date_generation).strftime('%d/%m/%Y %H:%M')}", styles["Normal"]))
    story.append(Spacer(1, 12))

    # En-tête du tableau
    data = [['Produit', 'Type de mouvement', 'Quantité', 'Date', 'Utilisateur']]

    # Contenu du tableau
    for m in mouvements:
        data.append([
            m.produit.nom,
            m.get_type_mouvement_display(),
            str(m.quantite),
            timezone.localtime(m.date_mouvement).strftime('%d/%m/%Y %H:%M'),
            m.utilisateur.username if m.utilisateur else '-'
        ])

    # Création du tableau
    table = Table(data, colWidths=[100, 100, 70, 100, 100])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#003366')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('BACKGROUND', (0, 1), (-1, -1), colors.whitesmoke),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
    ]))

    story.append(table)
    doc.build(story)

    pdf = buffer.getvalue()
    buffer.close()
    response.write(pdf)
    return response