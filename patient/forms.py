from django import forms
from django.contrib.auth.models import User
from .models import ProfilPatient, PaiementMobile


class InscriptionPatientForm(forms.ModelForm):

    username = forms.CharField(
        label="Nom utilisateur"
    )

    password = forms.CharField(
        widget=forms.PasswordInput
    )


    class Meta:

        model = ProfilPatient

        fields = [
            "nom",
            "prenom",
            "telephone",
            "sexe"
        ]


    def save(self, commit=True):

        patient = super().save(commit=False)

        username = self.cleaned_data["username"]
        password = self.cleaned_data["password"]


        user = User.objects.create_user(
            username=username,
            password=password
        )


        patient.user = user


        if commit:
            patient.save()


        return patient
class RendezVousPatientForm(forms.Form):
    
    date = forms.DateField(
        widget=forms.DateInput(
            attrs={
                "type": "date",
                "class": "form-control"
            }
        ),
        label="Date du rendez-vous"
    )

    plainte = forms.CharField(
        widget=forms.Textarea(
            attrs={
                "class": "form-control",
                "rows": 4
            }
        ),
        label="Motif de consultation"
    )


class PaiementMobileForm(forms.Form):
    montant = forms.DecimalField(
        label="Montant (FC)",
        max_digits=10,
        decimal_places=2,
        initial=15000,
        min_value=1,
    )
    provider = forms.ChoiceField(
        choices=PaiementMobile.PROVIDER_CHOICES,
        label="Opérateur",
    )
    numero_tel = forms.CharField(
        max_length=20,
        label="Numéro du téléphone",
    )
    rendezvous = forms.IntegerField(
        label="ID du rendez-vous",
        required=False,
        help_text="Optionnel : associez le paiement à un rendez-vous existant",
    )