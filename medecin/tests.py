from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from laboratoire.models import DemandeLaboratoire, ResultatLaboratoire, TestLaboratoire, ValeurResultat
from medecin.models import RendezVous, Specialiste
from reception.models import Patient as ReceptionPatient


class MedecinLabResultTests(TestCase):
    def test_consultation_page_shows_lab_result(self):
        user = User.objects.create_user(username="doctorlab", password="secret123")
        specialist = Specialiste.objects.create(
            user=user,
            nom="Dr. Lab",
            specialite="Cardiologie",
            telephone="0987654321",
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
        rendezvous = RendezVous.objects.create(
            patient=reception_patient,
            specialiste=specialist,
            date="2026-07-20",
            heure="10:00:00",
            statut="en_cours",
        )
        test = TestLaboratoire.objects.create(nom="Hémogramme", specialite="Cardiologie")
        valeur = ValeurResultat.objects.create(test=test, libelle="Normal")
        demande = DemandeLaboratoire.objects.create(
            rendezvous=rendezvous,
            test_demande=test,
            plainte_patient="Fatigue",
            statut="termine",
        )
        resultat = ResultatLaboratoire.objects.create(
            demande=demande,
            commentaire="Tout va bien",
        )
        resultat.valeurs.add(valeur)

        self.client.force_login(user)
        response = self.client.get(reverse("consultation", args=[rendezvous.id]))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Normal")
        self.assertContains(response, "Tout va bien")
