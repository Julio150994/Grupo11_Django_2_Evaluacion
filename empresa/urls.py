"""Rutas para la aplicación empresa."""
from django.urls import path
from empresa import views

urlpatterns = [
    path('',views.InicioEmpresaView.as_view(), name="page_inicio"),
    path('registro/',views.registrar_cliente, name="registro_cliente"),
    path('sign_in/', views.sign_in, name="users_login"),
    # path('logout/', views.sign_out,name="users_logout"),
]
