from django.test import TestCase
from django.urls import reverse
from .models import Produit, Categorie

# Create your tests here.

class ProduitViewsTest(TestCase):
    """
    Tests fonctionnels pour la gestion complète des produits (CRUD)
    """

    def setUp(self):

        # Création d’une catégorie de test
        self.categorie = Categorie.objects.create(nom="Informatique")

        # Création d’un produit de base
        self.produit = Produit.objects.create(
            nom="Ordinateur Dell",
            categorie=self.categorie,
            prix_achat=400000,
            prix_vente=450000,
            seuil_min=2,
            seuil_max=50,
            stock_actuel=10
        )

    # =====================================================
    # 🧾 TESTS DE LECTURE (READ)
    # =====================================================

    def test_liste_produits(self):
        """Vérifie que la liste des produits s'affiche correctement"""
        response = self.client.get(reverse('liste_produits'))
        self.assertEqual(response.status_code, 200)
        # self.assertIn(self.produit.nom, str(response.content))


    # =====================================================
    # ➕ TESTS DE CRÉATION (CREATE)
    # =====================================================

    def test_ajouter_produit(self):
        """Vérifie qu’un produit peut être ajouté avec succès"""
        data = {
            'nom': 'Clavier Logitech',
            'categorie': self.categorie.id,
            'prix_achat': 15000,
            'prix_vente': 20000,
            'seuil_min': 1,
            'seuil_max': 20,
            'stock_actuel': 5
        }
        response = self.client.post(reverse('ajouter_produit'), data)
        self.assertEqual(response.status_code, 302)  # redirection après ajout
        self.assertTrue(Produit.objects.filter(nom='Clavier Logitech').exists())

    # =====================================================
    # ✏️ TESTS DE MISE À JOUR (UPDATE)
    # =====================================================

    def test_modifier_produit(self):
        """Vérifie qu’un produit peut être modifié avec succès"""
        data = {
            'nom': 'Dell Inspiron',
            'reference': 'DL-001',
            'categorie': self.categorie.id,
            'prix_achat': 420000,
            'prix_vente': 480000,
            'code_barre': '1234567890',
            'seuil_min': 2,
            'seuil_max': 50,
            'stock_actuel': 12
        }
        response = self.client.post(reverse('modifier_produit', args=[self.produit.id]), data)
        self.assertEqual(response.status_code, 302)
        self.produit.refresh_from_db()
        self.assertEqual(self.produit.nom, 'Dell Inspiron')
        self.assertEqual(self.produit.prix_vente, 480000)

    # =====================================================
    # ❌ TESTS DE SUPPRESSION (DELETE)
    # =====================================================

    def test_supprimer_produit(self):
        """Vérifie qu’un produit peut être supprimé"""
        response = self.client.post(reverse('supprimer_produit', args=[self.produit.id]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Produit.objects.filter(id=self.produit.id).exists())
