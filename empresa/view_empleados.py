from django.core.checks import messages
from itertools import chain
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


def editar_empleados(request,id,idUsuario):
    print("Id de empleado: "+str(id))
    print("Id de usuario: "+str(idUsuario))
    
    #SELECT u.username, u.password, e.dni, e.nombre, e.apellidos, e.direccion, e.biografia
    # FROM Usuarios u,
    # Empleados e WHERE u.id = e.id_usuario and u.id = e.idUsuario;
    
    data_emp = Empleado.objects.filter(id=id)
    print("Empleado: "+str(data_emp))
    
    data_user = Usuario.objects.filter(id=idUsuario)
    print("Usuario: "+str(data_user))
    
    set_empleado = list(chain(data_emp,data_user))
    print(set_empleado)
    
    #usuario = UsuarioModelForm(instance = data_user)
    #empleado = EmpleadoModelForm(instance = data_emp)
    
    context = {
        'usuario':data_user,
        'empleado':data_emp
    }
    
    if request.POST:
        #usuario = UsuarioModelForm(request.POST, instance = data_user)
        #empleado = EmpleadoModelForm(request.POST, instance = data_emp)
        context = {
            'usuario':data_user,
            'empleado':data_emp
        }
        
        #if usuario.is_valid():
        username = request.POST['username']
        pwd = request.POST['password']
        
        nuevo_usuario = Usuario(username=username, password=pwd)
        nuevo_usuario.password = make_password(nuevo_usuario.password)
        nuevo_usuario.save()
        user = User.objects.create_user(username = username, password = pwd)
        user.save()

        #if empleado.is_valid():
        last_id_usuario = Usuario.objects.last()
        dni = request.POST.get("dni")
        nombre = request.POST.get("nombre")
        apellidos = request.POST.get("apellidos")
        direccion = request.POST.get("direccion")
        biografia = request.POST.get("biografia")
        idUsuario = request.POST.get("idUsuario",last_id_usuario)
            
        if dni is not None or nombre is not None or apellidos is not None or direccion is not None or biografia is not None or idUsuario is not None:
            set_empleado = Empleado(dni=dni, nombre=nombre, apellidos=apellidos, direccion=direccion,
                biografia=biografia,idUsuario=idUsuario)
            set_empleado.save()
            messages.success(request,'Empleado editado correctamente.')
            return redirect('empleados')
    
    return render(request,'empresa/form_edit_empleado.html',context)

def eliminar_empleados(request,id,idUsuario):
    empleado = Empleado.objects.filter(id=id)
    print(empleado)
    
    usuario = Usuario.objects.filter(id=idUsuario)    
    print(usuario)
    
    set_empleado = list(chain(empleado,usuario)) #combinamos las dos consultas haciendolo una#
    print(set_empleado)
    
    usuario.delete()
    empleado.delete()
    
    listEmpleados = Empleado.objects.all()
    context = {'empleados':listEmpleados}
    
    messages.error(request,'Empleado eliminado éxitosamente.')
    return render(request,'empresa/empleados.html',context)
