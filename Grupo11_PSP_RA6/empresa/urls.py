"""Rutas para la aplicación empresa."""
from django.urls import path
from empresa import views

urlpatterns = [
    path('',views.InicioEmpresaView.as_view(), name="page_inicio"),
]