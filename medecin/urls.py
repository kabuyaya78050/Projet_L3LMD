from django.urls import path
from . import views

urlpatterns = [
    path("login/", views.login_medecin, name="login_medecin"),
    path("register/", views.inscription_specialiste, name="inscription_specialiste"),
    path("dashboard/", views.dashboard_medecin, name="dashboard_medecin"),
    path("rdv/<int:id>/", views.detail_rdv, name="detail_rdv"),
    path("consultation/<int:id>/", views.consultation, name="consultation"),
    
]