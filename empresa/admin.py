from django.contrib import admin
from .models import Categoria, Empleado, Proyecto, Usuario, Cliente, Participa

class UsuariosAdmin(admin.ModelAdmin):
   #model = Usuario
   list_display = ("id","username","password")
    
class EmpleadoAdmin(admin.ModelAdmin):
    #model = Empleado
    list_display = ("id","dni","nombre","apellidos","direccion","biografia","idUsuario")
    
class ClienteAdmin(admin.ModelAdmin):
    #model = Cliente
    list_display = ("id","dni","nombre","apellidos","direccion","fechaNacimiento","fechaAlta","activo","idUsuario")

class CategoriaAdmin(admin.ModelAdmin):
    #model = Categoria
    list_display = ("id","nombre","foto")
class ProyectoAdmin(admin.ModelAdmin):
    #model = Proyecto
    list_display = ("id","titulo","descripcion","nivel","fechaInicio","fechaFin","idEmpleado","idCategoria")
    
class ParticipaAdmin(admin.ModelAdmin):
    #model = Participa
    list_display = ("id","idCliente","idProyecto","fechaInscripcion","rol")

# Register your models here.
admin.site.register(Usuario, UsuariosAdmin)
admin.site.register(Cliente, ClienteAdmin)
admin.site.register(Empleado, EmpleadoAdmin)
admin.site.register(Categoria, CategoriaAdmin)
admin.site.register(Proyecto, ProyectoAdmin)
admin.site.register(Participa, ParticipaAdmin)