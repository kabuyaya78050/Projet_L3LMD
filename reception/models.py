from django.db import models

class Patient(models.Model):

    nom = models.CharField(max_length=100)

    postnom = models.CharField(max_length=100)

    prenom = models.CharField(max_length=100)

    date_naissance = models.DateField()

    telephone = models.CharField(max_length=20)

    email = models.EmailField(blank=True, null=True)

    est_en_couple = models.BooleanField(default=False)

    nom_mari = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )

    statut = models.CharField(
        max_length=20,
        default='reception'
    )

    def __str__(self):
        return f"{self.nom} {self.postnom} {self.prenom}"