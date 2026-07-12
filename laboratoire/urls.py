from django.urls import path
from . import views

urlpatterns = [
    path("", views.dashboard_laboratoire, name="dashboard_laboratoire"),
    path("login/", views.login_laboratoire, name="login_laboratoire"),
    path("logout/", views.logout_laboratoire, name="logout_laboratoire"),

    path("detail/<int:id>/", views.detail_demande, name="detail_demande"),
    path("resultat/<int:id>/", views.resultat_laboratoire, name="resultat_laboratoire"),
]