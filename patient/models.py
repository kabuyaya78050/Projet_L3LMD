from django.db import models
from django.contrib.auth.models import User

from medecin.models import RendezVous


class ProfilPatient(models.Model):

    SEXE = [
        ('M', 'Masculin'),
        ('F', 'Féminin'),
    ]

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE
    )

    nom = models.CharField(
        max_length=100
    )

    prenom = models.CharField(
        max_length=100
    )

    telephone = models.CharField(
        max_length=20
    )

    date_naissance = models.DateField(
        null=True,
        blank=True
    )

    sexe = models.CharField(
        max_length=1,
        choices=SEXE
    )


    def __str__(self):
        return f"{self.nom} {self.prenom}"


class PaiementMobile(models.Model):

    PROVIDER_CHOICES = [
        ('orange_money', 'Orange Money'),
        ('m_pesa', 'M-Pesa'),
        ('airtel_money', 'Airtel Money'),
        ('wave', 'Wave'),
        ('wonyapay', 'Wonyapay'),
    ]

    STATUS_CHOICES = [
        ('pending', 'En attente'),
        ('paid', 'Payé'),
        ('failed', 'Échoué'),
    ]

    patient = models.ForeignKey(
        ProfilPatient,
        on_delete=models.CASCADE,
        related_name='paiements'
    )
    rendezvous = models.ForeignKey(
        RendezVous,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='paiements'
    )
    montant = models.DecimalField(max_digits=10, decimal_places=2, default=15000)
    provider = models.CharField(max_length=30, choices=PROVIDER_CHOICES, default='orange_money')
    numero_tel = models.CharField(max_length=20)
    reference = models.CharField(max_length=50, unique=True, blank=True, null=True)
    statut = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    date_creation = models.DateTimeField(auto_now_add=True)
    date_validation = models.DateTimeField(blank=True, null=True)
    note = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Paiement {self.reference or self.id} - {self.get_provider_display()}"