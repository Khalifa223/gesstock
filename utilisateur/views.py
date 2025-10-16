from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Utilisateur

# Create your views here.

def ajouter_utilisateur(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        role = request.POST.get('role')

        if Utilisateur.objects.filter(username=username).exists():
            messages.error(request, "Ce nom d’utilisateur existe déjà.")
            return redirect('ajouter_utilisateur')

        user = Utilisateur.objects.create_user(
            username=username,
            email=email,
            password=password,
            role=role
        )
        messages.success(request, f"Utilisateur {user.username} ajouté avec succès.")
        return redirect('liste_utilisateurs')

    return render(request, 'utilisateurs/ajouter_utilisateur.html', {'titre': 'Ajouter un utilisateur'})
