from django.contrib import admin
from .models import Categoria, Empleado, Proyecto, Usuario, Cliente, Participa

class UsuariosAdmin(admin.ModelAdmin):
    list_display = ("id","username","password")
    search_fields = ("username",)
    list_filter = ("username",)
    ordering = ("id",)
    
class EmpleadoAdmin(admin.ModelAdmin):
    list_display = ("id","dni","nombre","apellidos","direccion","biografia","idUsuario")
    search_fields = ("dni","nombre")
    list_filter = ("dni","nombre")
    ordering = ("id",)
    
class ClienteAdmin(admin.ModelAdmin):
    list_display = ("id","dni","nombre","apellidos","direccion","fechaNacimiento","fechaAlta","activo","idUsuario")
    search_fields = ("dni","nombre")
    list_filter = ("dni","nombre")
    ordering = ("id",)
    
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ("id","nombre","foto")
    search_fields = ("nombre",)
    list_filter = ("nombre",)
    ordering = ("id",)
    
class ProyectoAdmin(admin.ModelAdmin):
    list_display = ("id","titulo","descripcion","nivel","fechaInicio","fechaFin","idEmpleado","idCategoria")
    search_fields = ("titulo","nivel","idEmpleado","idCategoria")
    list_filter = ("titulo","idEmpleado","idCategoria")
    ordering = ("id",)
    
class ParticipaAdmin(admin.ModelAdmin):
    list_display = ("id","idCliente","idProyecto","fechaInscripcion","rol")
    search_fields = ("fechaInscripcion","rol")
    list_filter = ("rol",)
    ordering = ("id",)
    
# Register your models here.
admin.site.register(Usuario, UsuariosAdmin)
admin.site.register(Cliente, ClienteAdmin)
admin.site.register(Empleado, EmpleadoAdmin)
admin.site.register(Categoria, CategoriaAdmin)
admin.site.register(Proyecto, ProyectoAdmin)
admin.site.register(Participa, ParticipaAdmin)