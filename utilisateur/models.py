from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db import models
# Create your models here.

class Utilisateur(AbstractUser):
    ROLE_CHOICES = [
        ('ADMIN', 'Administrateur'),
        ('GESTIONNAIRE', 'Gestionnaire'),
        ('UTILISATEUR', 'Utilisateur simple'),
    ]
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='UTILISATEUR')

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"
