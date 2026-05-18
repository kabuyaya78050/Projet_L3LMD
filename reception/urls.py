from django.urls import path

from . import views

urlpatterns = [

    path(
        '',
        views.reception,
        name='reception'
    ),

    path(
        'ajouter/',
        views.ajoute,
        name='ajoute'
    ),

    path(
        'envoyer/<int:id>/',
        views.envoyer_medecin,
        name='envoyer_medecin'
    ),

]