"""Rutas para la aplicación empresa."""
from django.urls import path
from empresa import views, view_empleados, view_categorias

urlpatterns = [
    path('',views.InicioEmpresaView.as_view(), name="page_inicio"),
    path('registro/',views.registrar_cliente, name="registro_cliente"),
    path('sign_in/', views.sign_in, name="users_login"),
    path('logout/', views.sign_out, name="users_logout"),
    path('perfil_cliente/<int:id>/',views.vista_perfil, name="perfil_cliente"),
    
    path('empleados/',view_empleados.mostrar_empleados,name="empleados"),
    path('empleado/<int:id>/',view_empleados.datos_empleado,name="datos_empleado"),
    path('aniadir_empleado/',view_empleados.aniadir_empleado,name="form_add_empleado"),
    path('editar_empleado/<int:idUsuario>/',view_empleados.editar_empleado,name="form_edit_empleado"),
    path('eliminar_empleado/<int:id>/',view_empleados.eliminar_empleado,name="empleados"),
    
    path('categorias/',view_categorias.mostrar_categorias,name="categorias"),
    path('categoria/<int:id>/',view_categorias.datos_categoria,name="datos_categoria"),
    path('aniadir_categoria/',view_categorias.aniadir_categoria,name="form_add_categoria"),
    path('editar_categoria/<int:id>/',view_categorias.editar_categoria,name="form_edit_categoria"),
    path('eliminar_categoria/<int:id>/',view_categorias.eliminar_categoria,name="categorias"),
]
