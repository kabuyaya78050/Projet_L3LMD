from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect


def home(request):
    return redirect('login_medecin')


def redirect_patient_root(request):
    return redirect('connexion_patient')


urlpatterns = [
    path('', home),
    path('admin/', admin.site.urls),
    path('reception/', include('reception.urls')),
    path('medecin/', include('medecin.urls')),
    path('laboratoire/', include('laboratoire.urls')),
    path('patient/', include('patient.urls')),
    path('patient', redirect_patient_root),
    path('patient/', redirect_patient_root),
]