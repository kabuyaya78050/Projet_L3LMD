from django import forms
from django.contrib.auth import authenticate
from .models import ResultatLaboratoire, ValeurResultat


class LoginLaboratoireForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super().clean()

        username = cleaned_data.get("username")
        password = cleaned_data.get("password")

        user = authenticate(username=username, password=password)

        if not user:
            raise forms.ValidationError("Identifiants invalides")

        cleaned_data["user"] = user
        return cleaned_data


class ResultatLaboratoireForm(forms.ModelForm):

    class Meta:
        model = ResultatLaboratoire
        fields = ["valeurs", "commentaire", "statut"]

        widgets = {
            "valeurs": forms.CheckboxSelectMultiple(attrs={
                "class": "form-check-input"
            }),
            "commentaire": forms.Textarea(attrs={
                "class": "form-control",
                "rows": 4
            }),
            "statut": forms.Select(attrs={
                "class": "form-control"
            }),
        }

    def __init__(self, *args, **kwargs):
        test = kwargs.pop("test", None)
        super().__init__(*args, **kwargs)

        # N'afficher que les valeurs du test sélectionné
        if test:
            self.fields["valeurs"].queryset = ValeurResultat.objects.filter(test=test)