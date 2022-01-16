"""Rutas para la aplicación empresa."""
from django.urls import path
from empresa import views

urlpatterns = [
    path('',views.InicioEmpresaView.as_view(), name="page_inicio"),
    path('registro/',views.registrar_cliente, name="registro_cliente"),
    path('sign_in/', views.sign_in, name="users_login"),
    path('logout/', views.sign_out, name="users_logout"),
    path('perfil_cliente/<int:id>/',views.vista_perfil, name="perfil_cliente"),
    path('empleados/',views.mostrar_empleados,name="empleados"),
    path('empleado/<int:id>/',views.datos_empleado,name="datos_empleado"),
    path('add_empleado/',views.aniadir_empleado,name="form_empleado"),
    path('editar_empleado/<int:id>/',views.editar_empleado,name="form_empleado"),
    path('eliminar_empleado/<int:id>/',views.eliminar_empleado,name="empleados"),
]
