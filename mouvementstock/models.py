from django.db import models
from django.conf import settings
from produit.models import Produit
from fournisseur.models import Fournisseur
from client.models import Client
# Create your models here.

class MouvementStock(models.Model):
    TYPE_CHOICES = [
        ('ENTREE', 'Entrée'),
        ('SORTIE', 'Sortie'),
    ]

    produit = models.ForeignKey(Produit, on_delete=models.CASCADE, related_name="mouvements")
    type_mouvement = models.CharField(max_length=10, choices=TYPE_CHOICES)
    quantite = models.PositiveIntegerField()
    date_mouvement = models.DateTimeField(auto_now_add=True)
    commentaire = models.TextField(blank=True, null=True)
    utilisateur = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name="mouvements_effectues")
    fournisseur = models.ForeignKey(Fournisseur, on_delete=models.SET_NULL, null=True, blank=True)
    client = models.ForeignKey(Client, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.type_mouvement} - {self.produit.nom} ({self.quantite})"
