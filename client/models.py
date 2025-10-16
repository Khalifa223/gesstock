from django.db import models

# Create your models here.

class Client(models.Model):
    nom = models.CharField(max_length=150)
    contact = models.CharField(max_length=100, blank=True, null=True)
    adresse = models.TextField(blank=True, null=True)
    email = models.EmailField(blank=True, null=True)

    def __str__(self):
        return self.nom
