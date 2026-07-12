from django.db import models


class Patient(models.Model):

    STATUS_RECEPTION = 'reception'
    STATUS_ENVOYE = 'envoye'
    STATUS_EN_COURS = 'en_cours'
    STATUS_TERMINE = 'termine'
    STATUS_LABO = 'labo'

    STATUT_CHOICES = [
        (STATUS_RECEPTION, 'Réception'),
        (STATUS_ENVOYE, 'Envoyé au spécialiste'),
        (STATUS_EN_COURS, 'En cours de traitement'),
        (STATUS_TERMINE, 'Terminé'),
        (STATUS_LABO, 'Envoyé au laboratoire'),
    ]

    nom = models.CharField(max_length=100)
    postnom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)

    date_naissance = models.DateField()
    telephone = models.CharField(max_length=20)

    email = models.EmailField(blank=True, null=True)

    est_en_couple = models.BooleanField(default=False)
    nom_mari = models.CharField(max_length=100, blank=True, null=True)

    statut = models.CharField(
        max_length=30,
        choices=STATUT_CHOICES,
        default=STATUS_RECEPTION
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.nom} {self.postnom} {self.prenom}"