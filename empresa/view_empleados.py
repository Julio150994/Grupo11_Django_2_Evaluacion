from django.core.checks import messages
from django.urls import reverse
from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.views.generic.list import ListView
from empresa.models import Categoria, Cliente, Usuario, Empleado
from .forms import CategoriaModelForm, ClienteModelForm, EmpleadoModelForm, UsuarioModelForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User


def mostrar_empleados(request):
    listEmpleados = Empleado.objects.order_by('id').all()
    context = { 'empleados':listEmpleados }
    return render(request,'empresa/empleados.html',context)

def datos_empleado(request,id):
    empleado = Empleado.objects.get(id = id)
    context = {'empleado':empleado}
    return render(request,'empresa/datos_empleado.html',context)


def aniadir_empleado(request):
    usuario = UsuarioModelForm()
    empleado = EmpleadoModelForm()
    context = {
        'usuario':usuario,
        'empleado': empleado
    }
    
    if request.method == 'POST':
        usuario = UsuarioModelForm(request.POST)
        empleado = EmpleadoModelForm(request.POST)
        context = {
            'usuario': usuario,
            'empleado': empleado
        }
        
        if usuario.is_valid():
            username = request.POST['username']
            pwd = request.POST['password']
            usuario.save()
            
            nuevo_usuario = Usuario(username=username, password=pwd)
            nuevo_usuario.password = make_password(nuevo_usuario.password)
            nuevo_usuario.save()
            
            if empleado.is_valid():
                last_id_usuario = Usuario.objects.last()
                
                dni = request.POST.get("dni")
                nombre = request.POST.get("nombre")
                apellidos = request.POST.get("apellidos")
                direccion = request.POST.get("direccion")
                biografia = request.POST.get("biografia")
                idUsuario = request.POST.get("idUsuario",last_id_usuario)
                
                if dni is not None or nombre is not None or apellidos is not None or direccion is not None or biografia is not None or idUsuario is not None:
                    nuevo_empleado = Empleado(dni=dni, nombre=nombre, apellidos=apellidos, direccion=direccion,biografia=biografia,idUsuario=idUsuario)
                    nuevo_empleado.save()
                    messages.success(request,'Empleado añadido correctamente.')
                    return redirect('empleados')
                else:
                    messages.warning(request,'Faltan datos por introducir.')
                    return redirect('form_add_empleado')
                
    return render(request, "empresa/form_add_empleado.html",context)

def editar_empleado(request,idUsuario):
    print("Id de usuario: "+str(idUsuario))
    
    #SELECT u.username, u.password, e.dni, e.nombre, e.apellidos, e.direccion, e.biografia
    # FROM Usuarios u,
    # Empleados e WHERE u.id = e.id_usuario and u.id = e.idUsuario;
    
    datos_empleado = Empleado.objects.filter(idUsuario=idUsuario)
    print("Empleado: "+str(datos_empleado))
    
    datos_usuario = Usuario.objects.get(id=idUsuario)
    print("Usuario: "+str(datos_usuario))
    
    empleado = EmpleadoModelForm(instance = datos_empleado)
    usuario = UsuarioModelForm(instance = datos_usuario)
    
    context = {'empleado':empleado, 'usuario':usuario}
    
    if request.POST:
        usuario = UsuarioModelForm(request.POST, instance = datos_usuario)
        empleado = EmpleadoModelForm(request.POST, instance = datos_empleado)
        context = {
            'usuario':usuario,
            'empleado':empleado
        }
    
    return render(request,'empresa/form_edit_empleado.html',context)

"""def editar_empleado(request,idUsuario):
    datos_empleado = Empleado.objects.filter(idUsuario=idUsuario)
    print("Empleado: "+str(datos_empleado))
    
    datos_usuario = Usuario.objects.get(id=idUsuario)
    print("Usuario: "+str(datos_usuario))
    
    usuario = UsuarioModelForm(instance = datos_usuario)
    empleado = EmpleadoModelForm(instance = datos_empleado)
    context = {
        'idUsuario':usuario,
        'empleado':empleado
    }
    
    if request.POST:
        usuario = UsuarioModelForm(request.POST, instance = datos_usuario)
        empleado = EmpleadoModelForm(request.POST, instance = datos_empleado)
        context = {
            'idUsuario':usuario,
            'empleado':empleado
        }
        
        if usuario.is_valid():
            username = request.POST['username']
            pwd = request.POST['password']
            
            perfil = Usuario(username=username, password=pwd)
            perfil.password = make_password(perfil.password)
            perfil.save()
        
            if empleado.is_valid():
                last_id_empleado = Empleado.objects.last()
                
                dni = request.POST.get("dni")
                nombre = request.POST.get("nombre")
                apellidos = request.POST.get("apellidos")
                direccion = request.POST.get("direccion")
                biografia = request.POST.get("biografia")
                idUsuario = request.POST.get("idUsuario",last_id_empleado)
                
                if dni is not None or nombre is not None or apellidos is not None or direccion is not None or biografia is not None or idUsuario is not None:
                    set_empleado = Empleado(dni=dni, nombre=nombre, apellidos=apellidos, direccion=direccion,biografia=biografia,idUsuario=idUsuario)
                    set_empleado.save()
                    messages.success(request,'Empleado editado correctamente.')
                    return redirect('empleados')
                else:
                    messages.warning(request,'Faltan datos por introducir.')
                    return redirect('form_edit_empleado')
            else:
                print("No se ha podido editar el empleado")
        else:
            print("No se ha podido editar el empleado")
        
    return render(request,'empresa/form_edit_empleado.html',context)"""


def eliminar_empleado(request,id):
    empleado = Empleado.objects.get(id = id)
    context = {'empleado':empleado}
    
    if empleado is None:
        messages.warning(request,'No se ha podido eliminar este empleado.')
    else:
        empleado.delete()
        messages.error(request,'Empleado con id '+str(empleado)+' eliminado éxitosamente.')
    
    return render(request,'empresa/empleados.html',context)