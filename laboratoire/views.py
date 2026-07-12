from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout
from django.shortcuts import get_object_or_404, render, redirect

from .models import DemandeLaboratoire, ResultatLaboratoire
from .forms import ResultatLaboratoireForm, LoginLaboratoireForm


# =========================
# LOGIN
# =========================
def login_laboratoire(request):

    if request.method == "POST":
        form = LoginLaboratoireForm(request.POST)

        if form.is_valid():
            user = form.cleaned_data["user"]
            login(request, user)
            return redirect("dashboard_laboratoire")

    else:
        form = LoginLaboratoireForm()

    return render(request, "laboratoire/login.html", {"form": form})


# =========================
# LOGOUT
# =========================
def logout_laboratoire(request):
    logout(request)
    return redirect("login_laboratoire")


# =========================
# DASHBOARD
# =========================
def dashboard_laboratoire(request):

    demandes = DemandeLaboratoire.objects.all().order_by("-date_creation")

    return render(request, "laboratoire/dashboard.html", {
        "demandes": demandes,
        "total": demandes.count(),
        "attente": demandes.filter(statut="attente").count(),
        "encours": demandes.filter(statut="encours").count(),
        "termine": demandes.filter(statut="termine").count(),
    })


# =========================
# DETAIL DEMANDE
# =========================
def detail_demande(request, id):

    demande = get_object_or_404(DemandeLaboratoire, id=id)

    return render(request, "laboratoire/detail_demande.html", {
        "demande": demande
    })


# =========================
# RESULTAT (CREATE + UPDATE)
# =========================
def resultat_laboratoire(request, id):

    demande = get_object_or_404(DemandeLaboratoire, id=id)

    resultat_obj, created = ResultatLaboratoire.objects.get_or_create(
        demande=demande
    )

    if request.method == "POST":
        form = ResultatLaboratoireForm(request.POST, instance=resultat_obj)

        if form.is_valid():
            resultat = form.save(commit=False)
            resultat.demande = demande
            resultat.save()

            form.save_m2m()  # IMPORTANT pour ManyToMany (valeurs)

            demande.statut = "termine"
            demande.save()

            return redirect("dashboard_laboratoire")

    else:
        form = ResultatLaboratoireForm(instance=resultat_obj)

    return render(request, "laboratoire/resultat_form.html", {
        "form": form,
        "demande": demande
    })