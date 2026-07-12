from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from .models import Specialiste, RendezVous
from laboratoire.models import DemandeLaboratoire, TestLaboratoire


# ==========================
# INSCRIPTION SPECIALISTE
# ==========================

def inscription_specialiste(request):

    if request.method == "POST":

        nom = request.POST.get("nom")
        specialite = request.POST.get("specialite")
        username = request.POST.get("username")
        password = request.POST.get("password")


        if User.objects.filter(username=username).exists():

            return render(request, "auth/register.html", {
                "error": "Nom d'utilisateur déjà utilisé"
            })


        user = User.objects.create_user(
            username=username,
            password=password
        )


        Specialiste.objects.create(
            user=user,
            nom=nom,
            specialite=specialite
        )


        return redirect("login_medecin")


    return render(request, "auth/register.html")



# ==========================
# LOGIN SPECIALISTE
# ==========================

def login_medecin(request):

    if request.method == "POST":

        username = request.POST.get("username")
        password = request.POST.get("password")


        user = authenticate(
            request,
            username=username,
            password=password
        )


        if user:

            login(request, user)

            return redirect("dashboard_medecin")


        return render(request, "auth/login.html", {
            "error": "Identifiants incorrects"
        })


    return render(request, "auth/login.html")



# ==========================
# DASHBOARD SPECIALISTE
# ==========================

@login_required
def dashboard_medecin(request):

    specialiste = get_object_or_404(
        Specialiste,
        user=request.user
    )


    rendezvous = RendezVous.objects.filter(
        specialiste=specialiste
    ).order_by("-date", "-heure")


    return render(request, "specialiste/dashboard.html", {

        "specialiste": specialiste,
        "rendezvous": rendezvous

    })



# ==========================
# CREATION DEMANDE LABO
# ==========================

@login_required
def detail_rdv(request, id):

    specialiste = get_object_or_404(
        Specialiste,
        user=request.user
    )


    rdv = get_object_or_404(
        RendezVous,
        id=id,
        specialiste=specialiste
    )


    tests = TestLaboratoire.objects.all()



    if request.method == "POST":


        test_id = request.POST.get("test_demande")

        plainte = request.POST.get(
            "plainte_patient"
        )


        if test_id:


            test = get_object_or_404(
                TestLaboratoire,
                id=test_id
            )


            DemandeLaboratoire.objects.create(

                rendezvous=rdv,

                test_demande=test,

                plainte_patient=plainte

            )


            # changement statut patient

            rdv.patient.statut = "labo"

            rdv.patient.save()



            rdv.statut = "en_cours"

            rdv.save()



        return redirect(
            "dashboard_medecin"
        )



    return render(request,
        "specialiste/detail_rdv.html",
        {

            "rdv": rdv,

            "tests": tests

        }
    )




# ==========================
# CONSULTATION SPECIALISTE
# ==========================

@login_required
def consultation(request, id):


    specialiste = get_object_or_404(
        Specialiste,
        user=request.user
    )


    rdv = get_object_or_404(
        RendezVous,
        id=id,
        specialiste=specialiste
    )



    demandes_labo = DemandeLaboratoire.objects.filter(
        rendezvous=rdv,
        resultat_labo__isnull=False,
    ).order_by("-date_creation")



    return render(request,
        "specialiste/consultation.html",
        {

            "rdv": rdv,

            "demandes_labo": demandes_labo

        }
    )