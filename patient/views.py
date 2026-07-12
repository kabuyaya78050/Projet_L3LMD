import json
import os
import urllib.error
import urllib.request

from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.utils import timezone

from .forms import InscriptionPatientForm, RendezVousPatientForm, PaiementMobileForm
from .models import ProfilPatient, PaiementMobile
from medecin.models import RendezVous, Specialiste
from reception.models import Patient as ReceptionPatient


def _create_wonyapay_payment(amount, phone, reference, description="Consultation médicale"):
    api_key = (
        getattr(settings, "WONYAPAY_API_KEY", None)
        or os.getenv("WONYAPAY_API_KEY")
        or os.getenv("WONYAPAY_SECRET_KEY")
        or os.getenv("WONYAPAY_TOKEN")
        or ""
    )
    merchant_id = (
        getattr(settings, "WONYAPAY_MERCHANT_ID", None)
        or os.getenv("WONYAPAY_MERCHANT_ID")
        or os.getenv("WONYAPAY_MERCHANT")
        or os.getenv("WONYAPAY_ACCOUNT_ID")
        or ""
    )
    base_url = (
        getattr(settings, "WONYAPAY_BASE_URL", None)
        or os.getenv("WONYAPAY_BASE_URL")
        or os.getenv("WONYAPAY_API_URL")
        or "https://api.wonyapay.dev/mock/payments"
    )
    api_secret = os.getenv("WONYAPAY_API_SECRET", "")

    payload = {
        "merchant_id": merchant_id,
        "amount": float(amount),
        "currency": "USD",
        "phone_number": phone,
        "reference": reference,
        "description": description,
    }

    if api_secret:
        payload["api_secret"] = api_secret

    if not api_key or not merchant_id:
        return {
            "success": True,
            "status": "simulated",
            "reference": reference,
            "message": "Wonyapay credentials not configured; using local simulation",
        }

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}",
    }
    if api_secret:
        headers["X-Api-Secret"] = api_secret

    request = urllib.request.Request(
        base_url,
        data=json.dumps(payload).encode("utf-8"),
        headers=headers,
        method="POST",
    )

    try:
        with urllib.request.urlopen(request, timeout=10) as response:
            body = json.loads(response.read().decode("utf-8"))
            return {
                "success": True,
                "status": body.get("status") or "pending",
                "reference": body.get("reference") or reference,
                "message": body.get("message") or "Paiement Wonyapay envoyé",
            }
    except urllib.error.HTTPError as exc:
        return {
            "success": False,
            "status": "failed",
            "reference": reference,
            "message": f"Wonyapay error: {exc.code}",
        }
    except Exception as exc:
        return {
            "success": False,
            "status": "failed",
            "reference": reference,
            "message": f"Wonyapay request failed: {exc}",
        }


def _get_or_create_reception_patient(profil_patient):
    patient = ReceptionPatient.objects.filter(
        telephone=profil_patient.telephone
    ).first()

    if patient:
        return patient

    return ReceptionPatient.objects.create(
        nom=profil_patient.nom,
        postnom="",
        prenom=profil_patient.prenom,
        date_naissance=profil_patient.date_naissance or timezone.now().date(),
        telephone=profil_patient.telephone,
        email="",
        est_en_couple=False,
        nom_mari="",
        statut="reception",
    )


def inscription_patient(request):

    if request.method == "POST":

        form = InscriptionPatientForm(request.POST)

        if form.is_valid():

            form.save()

            return redirect(
                "connexion_patient"
            )

    else:

        form = InscriptionPatientForm()


    return render(
        request,
        "patient/inscription.html",
        {
            "form":form
        }
    )



def connexion_patient(request):

    if request.method == "POST":

        username = request.POST["username"]
        password = request.POST["password"]


        user = authenticate(
            username=username,
            password=password
        )


        if user:

            login(request,user)

            return redirect(
                "dashboard_patient"
            )


    return render(
        request,
        "patient/login.html"
    )

@login_required(login_url="connexion_patient")
def dashboard_patient(request):

    profil_patient = get_object_or_404(
        ProfilPatient,
        user=request.user
    )

    reception_patient = _get_or_create_reception_patient(profil_patient)

    rendezvous = RendezVous.objects.filter(
        patient=reception_patient
    ).order_by(
        "-date"
    )

    return render(
        request,
        "patient/dashboard.html",
        {
            "patient": profil_patient,
            "rendezvous": rendezvous,
            "total_rdv": rendezvous.count()
        }
    )

def deconnexion_patient(request):

    logout(request)

    return redirect(
        "connexion_patient"
    )


@login_required(login_url="connexion_patient")
def prendre_rendezvous(request):

    profil_patient = get_object_or_404(
        ProfilPatient,
        user=request.user
    )

    if request.method == "POST":

        form = RendezVousPatientForm(request.POST)

        if form.is_valid():
            reception_patient = _get_or_create_reception_patient(profil_patient)
            specialiste = Specialiste.objects.order_by("id").first()

            if specialiste:
                RendezVous.objects.create(
                    patient=reception_patient,
                    specialiste=specialiste,
                    date=form.cleaned_data["date"],
                    heure=timezone.now().time(),
                    statut="en_attente",
                    observation=form.cleaned_data["plainte"],
                )

                return redirect(
                    "dashboard_patient"
                )

    else:
        form = RendezVousPatientForm()

    return render(
        request,
        "patient/prendre_rendezvous.html",
        {
            "form": form
        }
    )


@login_required(login_url="connexion_patient")
def paiement_mobile(request):
    profil_patient = get_object_or_404(
        ProfilPatient,
        user=request.user
    )

    if request.method == "POST":
        form = PaiementMobileForm(request.POST)
        if form.is_valid():
            rendezvous = None
            rdv_id = form.cleaned_data.get("rendezvous")
            if rdv_id:
                rendezvous = get_object_or_404(RendezVous, id=rdv_id)

            reference = f"WNY-{timezone.now().strftime('%Y%m%d%H%M%S')}"
            gateway_result = None
            provider = form.cleaned_data["provider"]
            if provider == "wonyapay":
                gateway_result = _create_wonyapay_payment(
                    amount=form.cleaned_data["montant"],
                    phone=form.cleaned_data["numero_tel"],
                    reference=reference,
                )

            payment_status = "paid"
            note = "Paiement mobile simulé validé"
            if provider == "wonyapay":
                gateway_status = None
                gateway_message = None
                if gateway_result and hasattr(gateway_result, "get"):
                    gateway_status = gateway_result.get("status")
                    gateway_message = gateway_result.get("message")
                if gateway_status == "pending":
                    payment_status = "pending"
                if isinstance(gateway_message, str) and gateway_message:
                    note = gateway_message
                else:
                    note = "Paiement Wonyapay traité"

            PaiementMobile.objects.create(
                patient=profil_patient,
                rendezvous=rendezvous,
                montant=form.cleaned_data["montant"],
                provider=provider,
                numero_tel=form.cleaned_data["numero_tel"],
                reference=reference,
                statut=payment_status,
                note=note,
                date_validation=timezone.now() if payment_status == "paid" else None,
            )
            return redirect("dashboard_patient")
    else:
        form = PaiementMobileForm(initial={"montant": "15000"})

    return render(
        request,
        "patient/paiement_mobile.html",
        {
            "form": form,
            "patient": profil_patient,
        }
    )