"""Rutas para la aplicación empresa."""
from django.urls import path
from empresa import view_clientes, view_pry, views, view_empleados, view_categorias

urlpatterns = [
    path('',views.InicioEmpresaView.as_view(), name="page_inicio"),
    path('registro/',views.registrar_cliente, name="registro_cliente"),
    path('sign_in/', views.sign_in, name="users_login"),
    path('logout/', views.sign_out, name="users_logout"),
    path('perfil_cliente/<int:id>/',views.vista_perfil, name="perfil_cliente"),
    
    path('empleados/',view_empleados.mostrar_empleados,name="empleados"),
    path('empleado/<int:id>/',view_empleados.datos_empleado,name="datos_empleado"),
    path('annadir_empleado/',view_empleados.annadir_empleados,name="form_add_empleado"),
    path('editar_empleado/<int:id>/<int:idUsuario>/',view_empleados.editar_empleados,name="form_edit_empleado"),
    path('eliminar_empleado/<int:id>/<int:idUsuario>/',view_empleados.eliminar_empleados,name="empleados"),
    
    path('categorias/',view_categorias.mostrar_categorias,name="categorias"),
    path('categoria/<int:id>/',view_categorias.datos_categoria,name="datos_categoria"),
    path('annadir_categoria/',view_categorias.annadir_categorias,name="form_add_categoria"),
    path('editar_categoria/<int:id>',view_categorias.editar_categorias,name="form_edit_categoria"),
    path('eliminar_categoria/<int:id>/',view_categorias.eliminar_categorias,name="categorias"),
    #path('update_categoria/<int:id_categoria>',view_categorias.editar_categorias,name="categorias"),

    path('proyectos/',view_pry.mostrar_pry,name="proyectos"),
    path('annadir_proyecto/',view_pry.annadir_proyecto,name="form_add_pry"),
    # path('editar_proyecto/<int:id>/',view_pry.editar_proyecto,name="form_edit_pry"),
    path('historial_pry',view_pry.ver_historial_proyectos,name="historial_pry"),

    path('clientes/',view_clientes.mostrar_clientes,name="clientes"),
    path('cliente/<int:id>/',view_clientes.datos_cliente,name="datos_cliente"),
    path('annadir_clientes/',view_clientes.annadir_clientes,name="form_add_cliente"),
    path('editar_clientes/<int:id>/<int:idUsuario>/',view_clientes.editar_clientes,name="form_edit_cliente"),
    path('eliminar_cliente/<int:id>/<int:idUsuario>/',view_clientes.eliminar_cliente,name="delete"),
]
