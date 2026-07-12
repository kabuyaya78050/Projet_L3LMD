from django.db import models
from medecin.models import RendezVous, Specialiste
from reception.models import Patient
from django.contrib.auth.models import User


# =========================
# LABORANTIN
# =========================
class Laborantin(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nom = models.CharField(max_length=100)

    def __str__(self):
        return self.nom


# =========================
# TYPES DE TESTS
# =========================
class TestLaboratoire(models.Model):
    nom = models.CharField(max_length=150)
    specialite = models.CharField(max_length=100)

    def __str__(self):
        return self.nom


# =========================
# VALEURS POSSIBLES
# =========================
class ValeurResultat(models.Model):
    test = models.ForeignKey(
        TestLaboratoire,
        on_delete=models.CASCADE,
        related_name="valeurs"
    )
    libelle = models.CharField(max_length=200)

    def __str__(self):
        return f"{self.test.nom} - {self.libelle}"


# =========================
# DEMANDE DE LABORATOIRE
# =========================
class DemandeLaboratoire(models.Model):

    STATUTS = [
        ('attente', 'En attente'),
        ('encours', 'En cours'),
        ('termine', 'Terminé'),
        ('pret_medecin', 'Prêt médecin'),
    ]

    rendezvous = models.ForeignKey(
        RendezVous,
        on_delete=models.CASCADE,
        related_name="demandes_labo"
    )

    test_demande = models.ForeignKey(
        TestLaboratoire,
        on_delete=models.CASCADE
    )

    plainte_patient = models.TextField()

    statut = models.CharField(
        max_length=20,
        choices=STATUTS,
        default='attente'
    )

    date_creation = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.rendezvous.patient.nom} - {self.test_demande.nom}"


# =========================
# RESULTAT LABORATOIRE
# =========================
class ResultatLaboratoire(models.Model):
    
    STATUTS = [
        ('attente', 'En attente'),
        ('encours', 'En cours'),
        ('termine', 'Terminé'),
    ]

    demande = models.OneToOneField(
        DemandeLaboratoire,
        on_delete=models.CASCADE,
        related_name="resultat_labo"
    )

    valeurs = models.ManyToManyField(
        ValeurResultat,
        blank=True
    )

    commentaire = models.TextField(blank=True, null=True)

    statut = models.CharField(
        max_length=20,
        choices=STATUTS,
        default='termine'
    )

    date = models.DateTimeField(auto_now_add=True)