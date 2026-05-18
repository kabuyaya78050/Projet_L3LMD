from django.shortcuts import render, redirect

from .models import Patient
from .forms import PatientForm


# ==========================
# LISTE DES PATIENTS
# ==========================

def reception(request):

    recherche = request.GET.get('recherche')

    patients = Patient.objects.all().order_by('-id')

    if recherche:

        patients = patients.filter(
            nom__icontains=recherche
        )

    return render(request, 'reception.html', {

        'patients': patients

    })


# ==========================
# AJOUTER PATIENT
# ==========================

def ajoute(request):

    form = PatientForm()

    if request.method == 'POST':

        form = PatientForm(request.POST)

        if form.is_valid():

            form.save()

            return redirect('reception')

    return render(request, 'ajoute.html', {

        'form': form

    })


# ==========================
# ENVOYER MEDECIN
# ==========================

def envoyer_medecin(request, id):

    patient = Patient.objects.get(id=id)

    patient.statut = 'envoye'

    patient.save()

    return redirect('reception')