from django.test import TestCase
from django.urls import reverse
from .models import Fournisseur

# Create your tests here.

class FournisseurViewsTest(TestCase):
    """
    Tests fonctionnels CRUD pour les Fournisseurs.
    """
    
    def setUp(self):
                
        # Création de partenaires pour les tests
        self.fournisseur_test = Fournisseur.objects.create(
            nom="Tech Distributeur",
            contact="98765432",
            email="fournisseur@example.com",
            adresse="Bamako"
        )

    def test_liste_fournisseurs(self):
            """Test d'affichage de la liste des fournisseurs"""
            response = self.client.get(reverse('liste_fournisseurs'))
            self.assertEqual(response.status_code, 200)
            # self.assertIn(self.fournisseur_test.nom, str(response.content))

    def test_ajouter_fournisseur(self):
        """Test d’ajout d’un fournisseur"""
        data = {
            'nom': 'Global Tech',
            'contact': '44556677',
            'email': 'global@example.com',
            'adresse': 'Kayes'
        }
        response = self.client.post(reverse('ajouter_fournisseur'), data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Fournisseur.objects.filter(nom='Global Tech').exists())

    def test_modifier_fournisseur(self):
        """Test de modification d’un fournisseur"""
        data = {
            'nom': 'Tech Mali',
            'contact': '98765432',
            'email': 'techmali@update.com',
            'adresse': 'Bamako'
        }
        response = self.client.post(reverse('modifier_fournisseur', args=[self.fournisseur_test.id]), data)
        self.assertEqual(response.status_code, 302)
        self.fournisseur_test.refresh_from_db()
        self.assertEqual(self.fournisseur_test.nom, 'Tech Mali')

    def test_supprimer_fournisseur(self):
        """Test de suppression d’un fournisseur"""
        response = self.client.post(reverse('supprimer_fournisseur', args=[self.fournisseur_test.id]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Fournisseur.objects.filter(id=self.fournisseur_test.id).exists())