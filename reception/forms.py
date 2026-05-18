from django import forms
from .models import Patient

class PatientForm(forms.ModelForm):

    class Meta:

        model = Patient

        fields = [
            'nom',
            'postnom',
            'prenom',
            'date_naissance',
            'telephone',
            'email',
            'est_en_couple',
            'nom_mari'
        ]

        widgets = {
            'date_naissance': forms.DateInput(
                attrs={'type': 'date'}
            )
        }