from django import forms
from django.contrib.auth.models import User

from .models import Specialiste, RendezVous
from laboratoire.models import DemandeLaboratoire, ResultatLaboratoire

class SpecialisteForm(forms.ModelForm):
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = Specialiste
        fields = ['nom', 'specialite', 'telephone']

    def save(self, commit=True):
        user = User.objects.create_user(
            username=self.cleaned_data['username'],
            password=self.cleaned_data['password']
        )

        specialiste = super().save(commit=False)
        specialiste.user = user

        if commit:
            specialiste.save()

        return specialiste
class DemandeLaboratoireForm(forms.ModelForm):
    
    class Meta:
        model = DemandeLaboratoire
        fields = ['test_demande', 'plainte_patient']

        widgets = {
            'plainte_patient': forms.Textarea(attrs={
                'rows': 4,
                'placeholder': 'Décrivez la plainte du patient...'
            }),
        }

class ResultatLaboratoireForm(forms.ModelForm):

    class Meta:
        model = ResultatLaboratoire
        fields = ["commentaire", "statut"]

        widgets = {
            "commentaire": forms.Textarea(attrs={
                "class": "form-control",
                "rows": 5
            }),
            "statut": forms.Select(attrs={"class": "form-control"}),
        }