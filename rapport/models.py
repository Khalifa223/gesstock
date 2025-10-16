from django.db import models
from django.conf import settings
from produit.models import Produit
from mouvementstock.models import MouvementStock

# Create your models here.

class Rapport(models.Model):
    TYPE_CHOICES = [
        ('VENTES', 'Rapport de ventes'),
        ('ACHATS', 'Rapport d’achats'),
        ('PERTE', 'Rapport de pertes'),
        ('STOCK', 'Rapport de stock global'),
    ]

    type_rapport = models.CharField(max_length=20, choices=TYPE_CHOICES)
    date_generation = models.DateTimeField(auto_now_add=True)
    genere_par = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    produits = models.ManyToManyField(Produit, blank=True)
    mouvements = models.ManyToManyField(MouvementStock, blank=True)

    def __str__(self):
        return f"{self.get_type_rapport_display()} ({self.date_generation.strftime('%d/%m/%Y')})"
