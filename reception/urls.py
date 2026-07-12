from django.urls import path
from . import views

urlpatterns = [
    path('', views.reception, name='reception'),
    path('ajouter/', views.ajoute, name='ajoute'),
    path('envoyer/<int:id>/', views.envoye, name='envoyer_medecin'),
    path('modifier/<int:id>/', views.modifie, name='modifie'),
]