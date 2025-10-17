from django.contrib import admin
from .models import Rapport

# Register your models here.

class RapportAdmin(admin.ModelAdmin):
    list_display = ('type_rapport', 'date_generation', 'genere_par')    

admin.site.register(Rapport, RapportAdmin)