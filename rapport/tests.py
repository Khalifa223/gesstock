from django.test import TestCase, Client
from django.urls import reverse
from django.utils import timezone
from .models import Rapport
from .models import Produit
from .models import MouvementStock
from utilisateur.models import Utilisateur
from io import BytesIO

# Create your tests here.
class RapportViewsTest(TestCase):
    """
    Tests fonctionnels pour la gestion des rapports (création, affichage, export PDF/Excel/CSV)
    """

    def setUp(self):
        
        # Utilisateur connecté
        self.user = Utilisateur.objects.create_user(username='admin', password='1234')
        self.client = Client()
        self.client.login(username='admin', password='1234')

        # Produit de test
        self.produit = Produit.objects.create(
            nom="Ordinateur HP",
            prix_achat=450000,
            prix_vente=500000,
            stock_actuel=10
        )

        # Création d’un rapport de test
        self.rapport = Rapport.objects.create(
            # titre="Rapport Entrées",
            type_rapport="ENTREE",
            date_generation=timezone.now()
        )

        # Mouvement lié au rapport
        MouvementStock.objects.create(
            produit=self.produit,
            type_mouvement="ENTREE",
            quantite=5,
            date_mouvement=timezone.now(),
            utilisateur=self.user,
            rapport=self.rapport
        )

    # =====================================================
    # 🔍 TESTS DE CONSULTATION (READ)
    # =====================================================

    def test_liste_rapports(self):
        """Vérifie que la liste des rapports s'affiche correctement"""
        response = self.client.get(reverse('liste_rapports'))
        self.assertEqual(response.status_code, 200)
        # self.assertIn(self.rapport.titre, str(response.content))

    def test_detail_rapport(self):
        """Vérifie que le détail d’un rapport est consultable"""
        response = self.client.get(reverse('details_rapport', args=[self.rapport.id]))
        self.assertEqual(response.status_code, 200)
        # self.assertIn(self.rapport.type_rapport, str(response.content))

    # =====================================================
    # 🧾 TESTS DE CREATION (CREATE)
    # =====================================================

    def test_creer_rapport(self):
        """Vérifie qu’un rapport peut être créé"""
        data = {
            'titre': 'Rapport Sorties',
            'type_rapport': 'SORTIE',
            'date_generation': timezone.now()
        }
        response = self.client.post(reverse('generer_rapport'), data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Rapport.objects.filter(type_rapport='SORTIE').exists())

    # =====================================================
    # 🧹 TESTS DE SUPPRESSION
    # =====================================================

    def test_supprimer_rapport(self):
        """Vérifie qu’un rapport peut être supprimé"""
        response = self.client.post(reverse('supprimer_rapport', args=[self.rapport.id]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Rapport.objects.filter(id=self.rapport.id).exists())

    # =====================================================
    # 📤 TESTS D’EXPORTATION (CSV / EXCEL / PDF)
    # =====================================================

    def test_export_csv(self):
        """Vérifie que l’export CSV fonctionne"""
        response = self.client.get(reverse('exporter_rapport_csv', args=[self.rapport.id]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'text/csv')
        self.assertIn('Produit', response.content.decode())

    def test_export_excel(self):
        """Vérifie que l’export Excel fonctionne"""
        response = self.client.get(reverse('exporter_rapport_excel', args=[self.rapport.id]))
        self.assertEqual(response.status_code, 200)
        self.assertIn(
            'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            response['Content-Type']
        )
        # Le contenu doit être binaire (fichier Excel)
        self.assertIsInstance(response.content, bytes)

    def test_export_pdf(self):
        """Vérifie que l’export PDF fonctionne"""
        response = self.client.get(reverse('exporter_rapport_pdf', args=[self.rapport.id]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/pdf')
        # Le contenu PDF commence généralement par "%PDF"
        self.assertTrue(response.content.startswith(b'%PDF'))