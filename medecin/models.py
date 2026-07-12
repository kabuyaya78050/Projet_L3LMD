from django.db import models
from django.contrib.auth.models import User
from reception.models import Patient


# =========================
# SPECIALISTE
# =========================
class Specialiste(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="specialiste_profile"
    )
    nom = models.CharField(max_length=100)
    specialite = models.CharField(max_length=100)
    telephone = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return f"{self.nom} ({self.specialite})"


# =========================
# RENDEZ-VOUS
# =========================
class RendezVous(models.Model):

    STATUT_CHOICES = [
        ("en_attente", "En attente"),
        ("en_cours", "En cours"),
        ("termine", "Terminé"),
        ("annule", "Annulé"),
    ]

    patient = models.ForeignKey(
        Patient,
        on_delete=models.CASCADE,
        related_name="rendezvous"
    )

    specialiste = models.ForeignKey(
        Specialiste,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="rendezvous"
    )

    date = models.DateField()
    heure = models.TimeField()

    statut = models.CharField(
        max_length=20,
        choices=STATUT_CHOICES,
        default="en_attente"
    )

    observation = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.patient.nom} - {self.date} {self.heure}"


# =========================
# PRESCRIPTION
# =========================
class Prescription(models.Model):

    rendezvous = models.OneToOneField(
        RendezVous,
        on_delete=models.CASCADE,
        related_name="prescription"
    )

    specialiste = models.ForeignKey(
        Specialiste,
        on_delete=models.CASCADE,
        related_name="prescriptions"
    )

    diagnostic = models.TextField()
    traitement = models.TextField()
    conseils = models.TextField(blank=True, null=True)

    date_creation = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Prescription #{self.id} - {self.rendezvous.patient.nom}"


class DisponibiliteSpecialiste(models.Model):

    specialiste = models.ForeignKey(
        Specialiste,
        on_delete=models.CASCADE,
        related_name="disponibilites"
    )

    date = models.DateField()

    heure_debut = models.TimeField()

    heure_fin = models.TimeField()

    disponible = models.BooleanField(
        default=True
    )


    def __str__(self):
        return f"{self.specialiste.nom} - {self.date} {self.heure_debut}"