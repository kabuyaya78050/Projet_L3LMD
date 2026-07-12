from unittest.mock import patch

from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse

from medecin.models import RendezVous, Specialiste
from reception.models import Patient as ReceptionPatient
from .forms import InscriptionPatientForm
from .models import ProfilPatient, PaiementMobile


class PatientUrlsTests(TestCase):
    def test_patient_views_import_and_routes_are_available(self):
        self.assertEqual(reverse("connexion_patient"), "/patient/connexion/")
        self.assertEqual(reverse("inscription_patient"), "/patient/inscription/")
        self.assertEqual(reverse("prendre_rendezvous"), "/patient/prendre-rendezvous/")

    def test_dashboard_requires_login(self):
        response = self.client.get(reverse("dashboard_patient"))
        self.assertEqual(response.status_code, 302)
        self.assertIn("/patient/connexion/?next=/patient/dashboard/", response.url)

    def test_take_appointment_page_renders_for_authenticated_patient(self):
        user = User.objects.create_user(username="patientappt", password="secret123")
        ProfilPatient.objects.create(
            user=user,
            nom="Amani",
            prenom="Paul",
            telephone="0999999999",
            sexe="M",
        )
        self.client.force_login(user)
        response = self.client.get(reverse("prendre_rendezvous"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Prendre rendez-vous")

    def test_registration_form_does_not_include_birth_date(self):
        form = InscriptionPatientForm()
        self.assertNotIn("date_naissance", form.fields)

    def test_patient_root_redirects_to_login(self):
        response = self.client.get("/patient")
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/patient/connexion/")

    def test_payment_view_creates_mobile_payment(self):
        user = User.objects.create_user(username="patientpay", password="secret123")
        profil = ProfilPatient.objects.create(
            user=user,
            nom="Amani",
            prenom="Paul",
            telephone="0999999999",
            sexe="M",
        )
        reception_patient = ReceptionPatient.objects.create(
            nom="Amani",
            postnom="",
            prenom="Paul",
            date_naissance="1990-01-01",
            telephone="0999999999",
            email="",
            est_en_couple=False,
            nom_mari="",
            statut=ReceptionPatient.STATUS_RECEPTION,
        )
        specialist = Specialiste.objects.create(
            user=User.objects.create_user(username="specpay", password="secret123"),
            nom="Dr. Mbuyi",
            specialite="Cardiologie",
            telephone="0987654321",
        )
        rendezvous = RendezVous.objects.create(
            patient=reception_patient,
            specialiste=specialist,
            date="2026-07-15",
            heure="10:00:00",
            statut="en_attente",
        )

        self.client.force_login(user)
        response = self.client.post(
            reverse("paiement_mobile"),
            {
                "montant": "15000",
                "provider": "orange_money",
                "numero_tel": "0999999999",
                "rendezvous": rendezvous.id,
            },
        )

        self.assertEqual(response.status_code, 302)
        self.assertTrue(
            PaiementMobile.objects.filter(patient=profil, rendezvous=rendezvous).exists()
        )

    @patch("patient.views._create_wonyapay_payment")
    def test_wonyapay_provider_calls_gateway(self, mock_gateway):
        user = User.objects.create_user(username="patientwonya", password="secret123")
        ProfilPatient.objects.create(
            user=user,
            nom="Amani",
            prenom="Paul",
            telephone="0999999999",
            sexe="M",
        )
        reception_patient = ReceptionPatient.objects.create(
            nom="Amani",
            postnom="",
            prenom="Paul",
            date_naissance="1990-01-01",
            telephone="0999999999",
            email="",
            est_en_couple=False,
            nom_mari="",
            statut=ReceptionPatient.STATUS_RECEPTION,
        )
        specialist = Specialiste.objects.create(
            user=User.objects.create_user(username="specwonya", password="secret123"),
            nom="Dr. Wonya",
            specialite="Cardiologie",
            telephone="0987654321",
        )
        rendezvous = RendezVous.objects.create(
            patient=reception_patient,
            specialiste=specialist,
            date="2026-07-16",
            heure="11:00:00",
            statut="en_attente",
        )

        self.client.force_login(user)
        response = self.client.post(
            reverse("paiement_mobile"),
            {
                "montant": "20000",
                "provider": "wonyapay",
                "numero_tel": "0999999999",
                "rendezvous": rendezvous.id,
            },
        )

        self.assertEqual(response.status_code, 302)
        mock_gateway.assert_called_once()
