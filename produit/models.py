from django.db import models

class Categorie(models.Model):
    nom = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.nom


class Produit(models.Model):
    nom = models.CharField(max_length=150)
    reference = models.CharField(max_length=100, unique=True)
    categorie = models.ForeignKey(Categorie, on_delete=models.SET_NULL, null=True, related_name="produits")
    prix_achat = models.DecimalField(max_digits=10, decimal_places=2)
    prix_vente = models.DecimalField(max_digits=10, decimal_places=2)
    code_barre = models.CharField(max_length=100, blank=True, null=True)
    seuil_min = models.PositiveIntegerField(default=0)
    seuil_max = models.PositiveIntegerField(default=100)
    stock_actuel = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.nom

    def est_en_rupture(self):
        return self.stock_actuel <= self.seuil_min
