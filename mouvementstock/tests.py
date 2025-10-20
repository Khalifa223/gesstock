from django.test import TestCase
from django.urls import reverse
from .models import MouvementStock

# Create your tests here.

class MouvementStockViewsTest(TestCase):
    """
    Tests fonctionnels CRUD pour les Fournisseurs.
    """
    
    def setUp(self):
        pass