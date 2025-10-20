from django.shortcuts import render, redirect, get_object_or_404
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


def liste_utilisateurs(request):
    """
    Afficher la liste de tous les utilisateurs du système.
    (Accessible uniquement par l’admin ou le gestionnaire)
    """
    utilisateurs = Utilisateur.objects.all()
    return render(request, 'utilisateurs/liste_utilisateurs.html', {'utilisateurs': utilisateurs})


def modifier_utilisateur(request, id):
    """
    Modifier les informations d’un utilisateur existant (par un administrateur).
    """
    utilisateur = get_object_or_404(Utilisateur, id=id)

    if request.method == 'POST':
        utilisateur.username = request.POST.get('username')
        utilisateur.email = request.POST.get('email')
        utilisateur.role = request.POST.get('role')
        password = request.POST.get('password')

        if password:
            utilisateur.set_password(password)
        utilisateur.save()

        messages.success(request, f"Utilisateur {utilisateur.username} modifié avec succès.")
        return redirect('liste_utilisateurs')

    return render(request, 'utilisateurs/modifier_utilisateur.html', {
        'utilisateur': utilisateur,
        'titre': 'Modifier un utilisateur'
    })
    
    
def supprimer_utilisateur(request, id):
    """
    Supprimer un utilisateur du système (par un administrateur).
    """
    utilisateur = get_object_or_404(Utilisateur, id=id)

    if request.method == 'POST':
        utilisateur.delete()
        messages.success(request, "Utilisateur supprimé avec succès.")
        return redirect('liste_utilisateurs')

    return render(request, 'utilisateurs/supprimer_utilisateur.html', {'utilisateur': utilisateur})


def profil_utilisateur(request):
    """
    Afficher et mettre à jour le profil de l’utilisateur connecté.
    """
    utilisateur = request.user

    if request.method == 'POST':
        utilisateur.email = request.POST.get('email')
        utilisateur.first_name = request.POST.get('first_name')
        utilisateur.last_name = request.POST.get('last_name')

        password = request.POST.get('password')
        if password:
            utilisateur.set_password(password)
        utilisateur.save()

        messages.success(request, "Profil mis à jour avec succès.")
        return redirect('profil_utilisateur')

    return render(request, 'utilisateurs/profil.html', {'utilisateur': utilisateur})