from django.urls import path

from . import views


urlpatterns = [

    path(
        "inscription/",
        views.inscription_patient,
        name="inscription_patient"
    ),

    path(
        "connexion/",
        views.connexion_patient,
        name="connexion_patient"
    ),

    path(
        "dashboard/",
        views.dashboard_patient,
        name="dashboard_patient"
    ),

    path(
        "prendre-rendezvous/",
        views.prendre_rendezvous,
        name="prendre_rendezvous"
    ),

    path(
        "logout/",
        views.deconnexion_patient,
        name="logout_patient"
    ),

    path(
        "paiement-mobile/",
        views.paiement_mobile,
        name="paiement_mobile"
    ),

]