from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model

User = get_user_model()

# Create your tests here.

class UtilisateurViewsTest(TestCase):
    """
    Tests fonctionnels pour la gestion des utilisateurs (CRUD + Authentification)
    """

    def setUp(self):
        # Création d’un administrateur
        self.admin = User.objects.create_user(
            username="admin",
            password="1234",
            email="admin@example.com",
            role="ADMIN"
        )

        # Création d’un utilisateur standard
        self.user = User.objects.create_user(
            username="user1",
            password="userpass",
            email="user1@example.com",
            role="UTILISATEUR"
        )

        # Client de test
        self.client = Client()
        self.client.login(username='admin', password='1234')

    # =====================================================
    # 🧾 TESTS DE CONNEXION / DECONNEXION
    # =====================================================

    def test_connexion_utilisateur(self):
        """Vérifie qu’un utilisateur peut se connecter"""
        client = Client()
        response = client.post(reverse('connexion_utilisateur'), {
            'username': 'admin',
            'password': '1234'
        })
        self.assertEqual(response.status_code, 302)  # redirection après login

    def test_deconnexion_utilisateur(self):
        """Vérifie que la déconnexion fonctionne"""
        response = self.client.get(reverse('deconnexion_utilisateur'))
        self.assertEqual(response.status_code, 302)  # redirection après logout

    # =====================================================
    # 👥 TESTS DE LISTE DES UTILISATEURS
    # =====================================================

    def test_liste_utilisateurs(self):
        """Vérifie que la liste des utilisateurs s’affiche"""
        response = self.client.get(reverse('liste_utilisateurs'))
        self.assertEqual(response.status_code, 200)
        # self.assertIn(self.user.username, str(response.content))

    # =====================================================
    # ➕ TEST D’AJOUT D’UN UTILISATEUR
    # =====================================================

    def test_ajouter_utilisateur(self):
        """Vérifie que l’administrateur peut ajouter un utilisateur"""
        data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'pass123',
            'role': 'GESTIONNAIRE'
        }
        response = self.client.post(reverse('ajouter_utilisateur'), data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(username='testuser').exists())

    # =====================================================
    # ✏️ TEST DE MODIFICATION D’UN UTILISATEUR
    # =====================================================

    def test_modifier_utilisateur(self):
        """Vérifie qu’un administrateur peut modifier un utilisateur"""
        data = {
            'username': 'user1',
            'email': 'user1_update@example.com',
            'role': 'GESTIONNAIRE'
        }
        response = self.client.post(reverse('modifier_utilisateur', args=[self.user.id]), data)
        self.assertEqual(response.status_code, 302)
        self.user.refresh_from_db()
        self.assertEqual(self.user.email, 'user1_update@example.com')

    # =====================================================
    # ❌ TEST DE SUPPRESSION D’UN UTILISATEUR
    # =====================================================

    def test_supprimer_utilisateur(self):
        """Vérifie qu’un administrateur peut supprimer un utilisateur"""
        response = self.client.post(reverse('supprimer_utilisateur', args=[self.user.id]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(User.objects.filter(id=self.user.id).exists())

    # =====================================================
    # 👤 TEST DU PROFIL UTILISATEUR
    # =====================================================

    def test_profil_utilisateur(self):
        """Vérifie que l’utilisateur peut consulter et modifier son profil"""
        self.client.login(username='user1', password='userpass')
        response = self.client.post(reverse('profil_utilisateur'), {
            'first_name': 'Ali',
            'last_name': 'Koné',
            'email': 'ali.kone@example.com',
        })
        self.assertEqual(response.status_code, 302)
        self.user.refresh_from_db()
        self.assertEqual(self.user.first_name, 'Ali')
        self.assertEqual(self.user.email, 'ali.kone@example.com')