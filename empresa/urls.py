"""Rutas para la aplicación empresa."""
from django.urls import path
from empresa import view_clientes, view_participa, view_pry, views, view_empleados, view_categorias
from empresa.view_participa import InformeClientePDFView

urlpatterns = [
    path('',views.mostrar_inicio, name="page_inicio"),
    path('registro/',views.registrar_cliente, name="registro_cliente"),
    path('sign_in/', views.sign_in, name="users_login"),
    path('logout/', views.sign_out, name="users_logout"),
    path('perfil_cliente/<int:id>/',views.vista_perfil, name="perfil_cliente"),
    
    path('empleados/',view_empleados.mostrar_empleados,name="empleados"),
    path('annadir_empleado/',view_empleados.annadir_empleados,name="form_add_empleado"),
    path('editar_empleado/<int:id>',view_empleados.editar_empleados,name="form_edit_empleado"),
    path('eliminar_empleado/<int:id>/',view_empleados.eliminar_empleados,name="empleados"),
    
    path('categorias/',view_categorias.mostrar_categorias,name="categorias"),
    path('annadir_categoria/',view_categorias.annadir_categorias,name="form_add_categoria"),
    path('editar_categoria/<int:id>/',view_categorias.editar_categorias,name="form_edit_categoria"),
    path('eliminar_categoria/<int:id>/',view_categorias.eliminar_categorias,name="categorias"),

    path('proyectos/',view_pry.mostrar_pry,name="proyectos"),
    path('proyectos_cli/',view_pry.mostrar_pry_clientes,name="proyectos_cliente"),
    path('annadir_proyecto/<int:empleado_id>/',view_pry.annadir_proyecto,name="form_add_pry"),
    path('editar_proyecto/<int:id>/<int:empleado_id>/',view_pry.modificar_pry,name="form_edit_pry"),
    path('eliminar_proyecto/<int:id>/',view_pry.dar_baja_pry,name="proyectos"),
    path('historial_pry/<int:idUsuario>/',view_pry.ver_historial_proyectos,name="historial_pry"),
    path('inscripcion/<int:cliente_id>/',view_participa.annadir_inscripcion_pry, name="inscripcion_pry"),
    path('clientes_pry/<int:id>/',view_participa.mostrar_clientes_pry, name="ver_clientes_empleado"),
    path('proyectosLunes/',view_pry.proyectos_siguiente_lunes, name="pry_lunes"),
    path('finalizar_proyecto/<int:id>/',view_pry.finalizar_proyectos, name="pry_fin"),

    path('clientes/',view_clientes.mostrar_clientes,name="clientes"),
    path('annadir_clientes/',view_clientes.annadir_clientes,name="form_add_cliente"),
    path('editar_clientes/<int:id>/',view_clientes.editar_clientes,name="form_edit_cliente"),
    path('eliminar_cliente/<int:id>/',view_clientes.eliminar_cliente,name="delete"),
    path('actived/<int:id>/',view_clientes.get_actived, name="clientes"),
    
    path('buscar_cli/',view_participa.buscar_clientes_pry,name="buscar_clientes"),
    #path('informe_cli/<int:cliente_id>',view_participa.mostrar_informe_pdf, name="pdf"),
    path('informe_cli/<int:cliente_id>/',InformeClientePDFView.as_view(), name="pdf"),
]
