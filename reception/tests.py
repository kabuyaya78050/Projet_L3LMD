from django.test import TestCase

from reception.models import Patient


class PatientStatusTests(TestCase):
    def test_status_constants_match_expected_values(self):
        self.assertEqual(Patient.STATUS_RECEPTION, 'reception')
        self.assertEqual(Patient.STATUS_ENVOYE, 'envoye')
        self.assertEqual(Patient.STATUS_EN_COURS, 'en_cours')
        self.assertEqual(Patient.STATUS_TERMINE, 'termine')
        self.assertEqual(Patient.STATUS_LABO, 'labo')

    def test_get_statut_display_uses_label_from_choices(self):
        patient = Patient.objects.create(
            nom='Dupont',
            postnom='Jean',
            prenom='Pierre',
            date_naissance='1990-01-01',
            telephone='0123456789',
        )

        self.assertEqual(patient.get_statut_display(), 'Réception')

        patient.statut = Patient.STATUS_ENVOYE
        patient.save(update_fields=['statut'])

        self.assertEqual(patient.get_statut_display(), 'Envoyé au spécialiste')
