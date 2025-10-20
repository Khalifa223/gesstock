from django.test import TestCase
from django.urls import reverse
from .models import Client

# Create your tests here.

class ClientViewsTest(TestCase): 
    """
    Tests fonctionnels CRUD pour les Clients.
    """
    def setUp(self):
                
        # Création de partenaires pour les tests
        self.client_test = Client.objects.create(
            nom= 'Alpha',
            contact= '12345678',
            email= 'alpha@example.com',
            adresse= 'Bamako'
        )
        
    def test_liste_clients(self):
       """Test d'affichage de la liste des clients"""
       response = self.client.get(reverse('liste_clients'))
       self.assertEqual(response.status_code, 200)
    #    self.assertIn(self.client_test.contact, str(response.content))
       

    def test_ajouter_client(self):
            """Test d'ajout d'un nouveau client"""
            data = {
                'nom': 'Beta',
                'contact': '22233344',
                'email': 'beta@example.com',
                'adresse': 'Sikasso'
            }
            response = self.client.post(reverse('ajouter_client'), data)
            self.assertEqual(response.status_code, 302)
            self.assertTrue(Client.objects.filter(nom='Beta').exists())
            
            
    def test_modifier_client(self):
        """Test de modification d’un client"""
        data = {
            'nom': 'Alpha Group',
            'contact': '12345678',
            'email': 'alpha@update.com',
            'adresse': 'Koulikoro'
        }
        response = self.client.post(reverse('modifier_client', args=[self.client_test.id]), data)
        self.assertEqual(response.status_code, 302)
        self.client_test.refresh_from_db()
        self.assertEqual(self.client_test.nom, 'Alpha Group')
        
    
    def test_supprimer_client(self):
        """Test de suppression d’un fournisseur"""
        response = self.client.post(reverse('supprimer_client', args=[self.client_test.id]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Client.objects.filter(id=self.client_test.id).exists())