from django.contrib import admin
from .models import Categoria, Empleado, Proyecto, Usuario, Cliente


# Register your models here.
admin.site.register(Usuario)
admin.site.register(Cliente)
admin.site.register(Empleado)
admin.site.register(Categoria)
admin.site.register(Proyecto)