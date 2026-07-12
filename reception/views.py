from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone

from .models import Patient
from .forms import PatientForm

from medecin.models import RendezVous, Specialiste


# =========================
# LISTE PATIENTS (RECEPTION)
# =========================
def reception(request):

    recherche = request.GET.get('recherche')

    patients = Patient.objects.all().order_by('-id')

    if recherche:
        patients = patients.filter(nom__icontains=recherche)

    return render(request, 'reception.html', {
        'patients': patients
    })


# =========================
# AJOUT PATIENT
# =========================
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


# =========================
# ENVOYER VERS SPÉCIALISTE
# =========================
def envoye(request, id):

    patient = get_object_or_404(Patient, id=id)

    # tous les spécialistes pour le formulaire
    specialistes = Specialiste.objects.all()

    if request.method == "POST":

        specialiste_id = request.POST.get("specialiste")

        if not specialiste_id:
            return render(request, "envoye.html", {
                "patient": patient,
                "specialistes": specialistes,
                "error": "Veuillez sélectionner un spécialiste"
            })

        specialiste = get_object_or_404(Specialiste, id=specialiste_id)

        # changer statut patient
        patient.statut = Patient.STATUS_ENVOYE
        patient.save(update_fields=["statut"])

        # créer rendez-vous
        RendezVous.objects.create(
            patient=patient,
            specialiste=specialiste,
            date=timezone.now().date(),
            heure=timezone.now().time(),
            statut="en_attente"
        )

        return redirect('reception')

    return render(request, "envoye.html", {
        "patient": patient,
        "specialistes": specialistes
    })


# =========================
# MODIFIER PATIENT
# =========================
def modifie(request, id):

    patient = get_object_or_404(Patient, id=id)

    form = PatientForm(instance=patient)

    if request.method == 'POST':
        form = PatientForm(request.POST, instance=patient)

        if form.is_valid():
            form.save()
            return redirect('reception')

    return render(request, 'modifie.html', {
        'form': form
    })