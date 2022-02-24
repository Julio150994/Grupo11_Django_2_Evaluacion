from django.core.checks import messages
from itertools import chain
from django.urls import reverse
from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.views.generic.list import ListView
from empresa.decorators import Admin
from empresa.models import Categoria, Cliente, Usuario, Empleado
from .forms import CategoriaModelForm, ClienteModelForm, EmpleadoModelForm, UsuarioModelForm
from django.contrib import messages
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User

@Admin
def mostrar_empleados(request):
    listEmpleados = Empleado.objects.order_by('-id').all()
    context = { 'empleados':listEmpleados }
    return render(request,'empresa/empleados.html',context)


def annadir_empleados(request):
    usuario = UsuarioModelForm()
    empleado = EmpleadoModelForm()
    context = {
        'usuario': usuario,
        'empleado': empleado
    }
    
    if request.POST:
        usuario = UsuarioModelForm(request.POST)
        empleado = EmpleadoModelForm(request.POST)
        context = {
            'usuario': usuario,
            'empleado': empleado
        }
        
        if usuario.is_valid():
            username = request.POST['username']
            pwd = request.POST['password']
            
            nuevo_usuario = Usuario(username=username, password=pwd)
            nuevo_usuario.password = make_password(nuevo_usuario.password)
            nuevo_usuario.save()
            user = User.objects.create_user(username = username, password = pwd)
            user.save()
            
            if empleado.is_valid():
                last_id_usuario = Usuario.objects.last()
                dni = request.POST.get("dni")
                nombre = request.POST.get("nombre")
                apellidos = request.POST.get("apellidos")
                direccion = request.POST.get("direccion")
                biografia = request.POST.get("biografia")
                idUsuario = request.POST.get("idUsuario",last_id_usuario)
                    
                if dni is not None or nombre is not None or apellidos is not None or direccion is not None or biografia is not None or idUsuario is not None:
                    nuevo_empleado = Empleado(dni=dni, nombre=nombre, apellidos=apellidos, direccion=direccion,
                        biografia=biografia,idUsuario=idUsuario)
                    
                    nuevo_empleado.save()
                    
                    messages.success(request,'Empleado añadido correctamente.')
                    return redirect('empleados')
            else:
                messages.warning(request,'Faltan datos de empleado por introducir.')
                return redirect('form_add_empleado')
        else:
            messages.warning(request,'Faltan datos de usuario por introducir.')
            return redirect('form_add_empleado')
                
    return render(request, "empresa/form_add_empleado.html",context)

def editar_empleados(request,id):
    id_empleado = Empleado.objects.get(id = id)
    context = {'empleado':id_empleado}
    
    if request.method == 'POST':
        empleado = EmpleadoModelForm(request.POST, instance = id_empleado)
        context = {
            'empleado': empleado
        }
        
        if empleado.is_valid():            
            dni = request.POST.get("dni")
            nombre = request.POST.get("nombre")
            apellidos = request.POST.get("apellidos")
            direccion = request.POST.get("direccion")
            biografia = request.POST.get("biografia")
            idUsuario = request.POST.get("idUsuario")
            username = request.POST.get("username")
            password = request.POST.get("password")
                
            if dni is not None or nombre is not None or apellidos is not None or direccion is not None or biografia is not None or idUsuario is not None:                
                empleado.save()         
                messages.success(request,'Empleado editado correctamente.')
                return redirect('empleados')
        else:
            messages.warning(request,'Faltan datos por introducir.')
            return redirect('empleados')
            
    return render(request,'empresa/form_edit_empleado.html',context)


def eliminar_empleados(request,id):    
    empleado = Empleado.objects.filter(id=id)
    print(empleado)
    
    
    # set_empleado = list(chain(empleado,usuario)) #combinamos las dos consultas haciendolo una#
    # print(set_empleado)
    
    empleado.delete()
    
    messages.error(request,'Empleado eliminado éxitosamente.')
    return redirect('empleados')